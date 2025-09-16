import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
import re # Import the regular expression module
import logging

# --- Configuration ---
load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(script_dir, "data", "monthly_simulation_log.csv")
API_KEY = os.getenv("GEMINI_API_KEY")

# --- We need the simulation parameters to calculate pace ---
SIMULATION_START_DATE = datetime(2025, 9, 1)
SIMULATION_MONTH_DAYS = 30
DAILY_HOURS_PER_TRAIN = 16

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please create a .env file with your key.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app)  # Allow requests from your React frontend

# --- Logging Setup ---
logging.basicConfig(
    filename='chatbot_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite log on each start
)

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
    """
    context_df = log_df[(log_df['simulation_day'] == day) & (log_df['train_id'].isin(train_ids))]
    if context_df.empty:
        return "No data found for the specified trains on that day.", ""
    
    # Create a detailed summary string for each train to help the AI understand "why"
    context_summary = ""
    for _, row in context_df.iterrows():
        status = row.get('status', 'N/A')
        health = row.get('health_score', 'N/A')
        fatigue = row.get('consecutive_service_days', 0)
        
        context_summary += f"\n- On Day {day}, {row['train_id']} was assigned to: **{status}**."
        context_summary += f"  - Its health score was {health:.1f}."
        if status == 'SERVICE':
             context_summary += f" It had been in service for {fatigue} consecutive day(s)."
        if status == 'MAINTENANCE':
            context_summary += " It was likely sent for maintenance because its health was low or it was manually flagged."
        if status == 'STANDBY':
            context_summary += " It was likely on standby because it was not needed for service or was less optimal than other trains."

    return context_df.to_string(index=False), context_summary

# --- The Main API Endpoint ---
@app.route('/chat', methods=['POST'])
def ask_rake_assist():
    logging.info("--- New Request Received ---")
    try:
        data = request.json
        user_question = data.get('message')
        logging.info(f"Request data: {data}")

        if not user_question:
            logging.warning("No user question provided.")
            return jsonify({"error": "No question provided."}), 400

        try:
            log_df = pd.read_csv(LOG_FILE)
            logging.info(f"Successfully loaded log file: {LOG_FILE}")
        except FileNotFoundError:
            logging.error(f"Log file not found: {LOG_FILE}")
            return jsonify({"error": f"Log file '{LOG_FILE}' not found."}), 500

        simulation_day = extract_day_from_question(user_question)
        logging.info(f"Extracted day: {simulation_day}")

        mentioned_train_ids = re.findall(r'rake-\d+', user_question, re.IGNORECASE)
        logging.info(f"Extracted train IDs: {mentioned_train_ids}")

        if not mentioned_train_ids:
            logging.info("No train IDs mentioned. Returning prompt.")
            return jsonify({"reply": "Please mention a specific train ID (e.g., Rake-03) in your question."})

        context_data, context_summary = get_context_for_query(log_df, simulation_day, mentioned_train_ids)
        logging.info(f"Context summary generated: {context_summary}")
        
        prompt = f"""
        You are RakeAssist, an expert AI co-pilot for the Kochi Metro operations supervisor. Your role is to answer questions concisely, accurately, and helpfully, using ONLY the data provided below as your context. Your primary task is to explain the "why" behind a decision.

        **Current Simulation Parameters:**
        - Today is Day {simulation_day} of a {SIMULATION_MONTH_DAYS}-day month.

        **Context Data for Day {simulation_day}:**
        ---
        {context_data}
        ---
        
        **Summary of Assignments:**
        {context_summary}

        **Analysis Task:**
        Based on the supervisor's question, analyze the provided data to explain WHY a train had a specific assignment.
        - If a train is in MAINTENANCE, it's because its health score was very low or it was manually flagged.
        - If a train is on STANDBY, it was a less optimal choice for service that day.
        - If a train is in SERVICE, it was one of the most cost-effective and healthy options available.
        Use the summary to state the assignment, then use the detailed context data to find the reason.

        **Supervisor's Question:** "{user_question}"

        **Your Answer:**
        """
        logging.debug(f"Generated Prompt:\n{prompt}")

        response = model.generate_content(prompt)
        ai_answer = response.text
        logging.info(f"Received response from Gemini: {ai_answer}")
        
        return jsonify({"reply": ai_answer})

    except Exception as e:
        logging.exception("An unexpected error occurred in /chat endpoint")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)

