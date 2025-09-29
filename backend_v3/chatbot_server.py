import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
import re # Import the regular expression module

# --- Configuration ---
load_dotenv()
LOG_FILE = "monthly_simulation_log.csv"  # CSV file with columns: simulation_day,train_id,status,health_score,consecutive_service_days,scenario
API_KEY = os.getenv("GEMINI_API_KEY")

# --- We need the simulation parameters to calculate pace ---
SIMULATION_START_DATE = datetime(2025, 9, 1)
SIMULATION_MONTH_DAYS = 30
DAILY_HOURS_PER_TRAIN = 16

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please create a .env file with your key.")

genai.configure(api_key=API_KEY)

# Try Gemini 2.5 Pro with fallback
def get_model():
    model_names = [
        'gemini-2.0-flash-exp',  # Latest Gemini 2.0 flash experimental
        'gemini-exp-1206',       # Gemini 2.5 Pro experimental
        'gemini-1.5-pro-latest', # Latest 1.5 Pro
        'gemini-1.5-pro',        # Standard 1.5 Pro
        'gemini-1.5-flash'       # Fallback flash model
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple query
            test_response = model.generate_content("Hello")
            print(f"✅ Successfully connected to model: {model_name}")
            return model
        except Exception as e:
            print(f"❌ Model {model_name} failed: {str(e)}")
            continue
    
    return None

model = get_model()
if not model:
    print("❌ Could not connect to any Gemini model. Please check your API key and model availability.")
    raise ValueError("No available Gemini model found")

app = Flask(__name__)
CORS(app)  # Allow requests from your React frontend

# --- Helper Functions ---

def extract_day_from_question(question, default_day=15):
    """
    Parses a question to find a specific day number.
    e.g., "what happened on day 13" -> 13
    """
    match = re.search(r'day\s+(\d+)', question, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return default_day

def get_context_for_query(log_df, day, train_ids):
    """
    Finds the relevant rows and creates a rich summary for the AI.
    Expected CSV columns: simulation_day,train_id,status,health_score,consecutive_service_days,scenario
    """
    # Filter data for the specific day and train IDs
    context_df = log_df[(log_df['simulation_day'] == day) & (log_df['train_id'].isin(train_ids))]
    
    if context_df.empty:
        return "No data found for the specified trains on that day.", ""
    
    # Create a detailed summary string for each train to help the AI understand "why"
    context_summary = ""
    detailed_data = []
    
    for _, row in context_df.iterrows():
        train_id = row['train_id']
        status = row['status']
        health_score = row['health_score']
        consecutive_days = row['consecutive_service_days']
        scenario = row['scenario']
        
        # Build summary explanation
        context_summary += f"\n- On Day {day}, {train_id} was assigned to: **{status}**"
        context_summary += f"\n  • Health Score: {health_score:.1f}/100"
        context_summary += f"\n  • Consecutive Service Days: {consecutive_days}"
        context_summary += f"\n  • Scenario: {scenario}"
        
        # Add reasoning based on status and metrics
        if status == 'SERVICE':
            if consecutive_days > 0:
                context_summary += f"\n  • This train had been in continuous service for {consecutive_days} day(s)"
            if health_score > 80:
                context_summary += f"\n  • High health score ({health_score:.1f}) made it suitable for service"
            elif health_score < 60:
                context_summary += f"\n  • Despite lower health ({health_score:.1f}), it was needed for service"
                
        elif status == 'MAINTENANCE':
            if health_score < 70:
                context_summary += f"\n  • Low health score ({health_score:.1f}) triggered maintenance requirement"
            if consecutive_days >= 3:
                context_summary += f"\n  • Extended service period ({consecutive_days} days) required maintenance break"
            context_summary += f"\n  • Maintenance was necessary to restore operational capability"
            
        elif status == 'STANDBY':
            context_summary += f"\n  • Kept in standby as backup or due to optimal fleet allocation"
            if health_score < 80:
                context_summary += f"\n  • Moderate health score ({health_score:.1f}) made it less priority for active service"
        
        context_summary += "\n"
        
        # Store detailed data for tabular display
        detailed_data.append({
            'Train ID': train_id,
            'Status': status,
            'Health Score': f"{health_score:.1f}",
            'Consecutive Service Days': consecutive_days,
            'Scenario': scenario
        })
    
    # Create formatted table for context
    formatted_table = pd.DataFrame(detailed_data).to_string(index=False)
    
    return formatted_table, context_summary

# --- Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    """Check if the chatbot service is healthy"""
    try:
        if not model:
            return jsonify({"status": "unhealthy", "message": "AI model not initialized"}), 503
        
        # Test if CSV file exists
        if not os.path.exists(LOG_FILE):
            return jsonify({"status": "unhealthy", "message": "Simulation data not found"}), 503
        
        return jsonify({"status": "healthy", "message": "RakeAssist AI is ready"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "message": str(e)}), 503

# --- The Main API Endpoint ---
@app.route('/ask', methods=['POST'])
def ask_rake_assist():
    data = request.json
    user_question = data.get('question')

    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    try:
        log_df = pd.read_csv(LOG_FILE)
        # Ensure we have the expected columns
        required_columns = ['simulation_day', 'train_id', 'status', 'health_score', 'consecutive_service_days', 'scenario']
        missing_columns = [col for col in required_columns if col not in log_df.columns]
        if missing_columns:
            return jsonify({"error": f"Missing required columns in CSV: {missing_columns}"}), 500
    except FileNotFoundError:
        return jsonify({"error": f"Log file '{LOG_FILE}' not found. Please ensure the simulation data is available."}), 500
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 500

    # Extract the day from the question
    simulation_day = extract_day_from_question(user_question)
    
    # Find mentioned train IDs in the question
    mentioned_train_ids = [word for word in user_question.replace(",", " ").split() if 'Rake-' in word]
    if not mentioned_train_ids:
        return jsonify({"answer": "Please mention a specific train ID (e.g., Rake-03) in your question to get detailed information."})

    # Validate that the requested day exists in the data
    available_days = sorted(log_df['simulation_day'].unique())
    if simulation_day not in available_days:
        return jsonify({"answer": f"Day {simulation_day} not found in simulation data. Available days: {min(available_days)}-{max(available_days)}"})

    # Get context for the specific trains and day
    context_data, context_summary = get_context_for_query(log_df, simulation_day, mentioned_train_ids)
    days_remaining = SIMULATION_MONTH_DAYS - simulation_day + 1

    # Enhanced AI prompt for better analysis
    prompt = f"""
    You are RakeAssist, an expert AI co-pilot for the Kochi Metro operations supervisor. Your role is to analyze train assignment data and explain operational decisions clearly and accurately.

    **Current Simulation Context:**
    - Day {simulation_day} of {SIMULATION_MONTH_DAYS} in the simulation
    - Each service train operates approximately {DAILY_HOURS_PER_TRAIN} hours per day
    - Health scores range from 0-100 (higher is better)
    - Consecutive service days indicate operational fatigue

    **Data Structure:**
    The data contains: simulation_day, train_id, status, health_score, consecutive_service_days, scenario

    **Raw Data for Day {simulation_day}:**
    {context_data}

    **Detailed Analysis:**
    {context_summary}

    **Decision Logic Guidelines:**
    1. **SERVICE Assignment**: Usually given to trains with good health scores (70+) and manageable fatigue
    2. **MAINTENANCE Assignment**: Triggered by low health scores (<70), high consecutive service days (3+), or scheduled maintenance
    3. **STANDBY Assignment**: For backup trains, lower priority trains, or those awaiting assignment

    **Health Score Ranges:**
    - 90-100: Excellent condition, priority for service
    - 70-89: Good condition, suitable for service
    - 50-69: Fair condition, may need attention soon
    - Below 50: Poor condition, likely requires maintenance

    **Question to Answer:** "{user_question}"

    **Instructions:**
    - Provide a direct answer about the train's status and assignment
    - Explain the reasoning based on the health score, consecutive service days, and scenario
    - Be specific about the numbers from the data
    - Keep the response professional but conversational
    - If multiple trains are mentioned, address each one

    **Your Response:**
    """

    try:
        if not model:
            return jsonify({"answer": "Sorry, the AI model is not available right now. Please check the server logs for model initialization errors."}), 503
        
        response = model.generate_content(prompt)
        ai_answer = response.text
        return jsonify({"answer": ai_answer})
    except Exception as e:
        error_msg = str(e)
        print(f"Error calling Gemini API: {error_msg}")
        
        # Provide more specific error messages
        if "404" in error_msg or "not found" in error_msg.lower():
            return jsonify({"answer": "The AI model is temporarily unavailable. This might be due to API quota limits or model availability. Please try again later or contact your administrator."}), 503
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return jsonify({"answer": "API quota exceeded. Please check your Google AI Studio quota or try again later."}), 429
        elif "api key" in error_msg.lower():
            return jsonify({"answer": "API key issue detected. Please verify your Gemini API key configuration."}), 401
        else:
            return jsonify({"answer": f"AI service temporarily unavailable. Error: {error_msg}"}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)  # Changed to port 5002 to avoid conflict