from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import json
import numpy as np

# Import from your final optimizer_engine.py
from answer_final import (
    run_simulation,
    initialize_fleet_status,
    AI_STRATEGIST_MODEL
)

app = Flask(__name__)
CORS(app)
MASTER_LOG_FILE = "simulation_log_master.json"

# Helper function to handle special number types for JSON
# In backend.py

# Helper function to handle special number types for JSON
def default_converter(o):
    # Handle NumPy integers
    if isinstance(o, (np.int64, np.int32, np.int16, np.int8)):
        return int(o)
    # Handle NumPy floats  
    if isinstance(o, (np.float64, np.float32, np.float16)):
        return float(o)
    # Handle NumPy arrays
    if isinstance(o, np.ndarray):
        return o.tolist()
    # Handle NumPy booleans
    if isinstance(o, np.bool_):
        return bool(o)
    # Handle any other NumPy scalar types
    if hasattr(o, 'item'):
        return o.item()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


@app.route('/run_full_simulation', methods=['POST'])
def api_run_full_simulation():
    print("Received request to run a full simulation.")
    initialize_fleet_status()
    initial_fleet_df = pd.read_csv("fleet_status.csv")
    
    features = ['total_fleet_size', 'target_service_trains', 'avg_fleet_health', 'is_monsoon', 'is_surge']
    targets = ['historical_cost_per_km', 'historical_fatigue_factor', 'historical_branding_penalty', 'historical_target_mileage', 'historical_maint_threshold']

    full_log = run_simulation(
        start_day=1,
        initial_fleet_state=initial_fleet_df,
        ai_model=AI_STRATEGIST_MODEL,
        feature_names=features,
        targets=targets
    )
    
    with open(MASTER_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(full_log, f, indent=2, default=default_converter, ensure_ascii=False)
        
    print(f"Full simulation complete. Log saved to {MASTER_LOG_FILE}")
    return jsonify({"status": "success", "message": "Full simulation complete."})


@app.route('/get_simulation_data', methods=['GET'])
def api_get_simulation_data():
    if not os.path.exists(MASTER_LOG_FILE):
        return jsonify({"status": "error", "message": "No simulation data found. Run a simulation first."}), 404
        
    try:
        with open(MASTER_LOG_FILE, 'r') as f:
            master_log = json.load(f)
        return jsonify({"status": "success", "data": master_log})
    except json.JSONDecodeError as e:
        return jsonify({"status": "error", "message": f"Invalid JSON in log file: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/rerun_from_day', methods=['POST'])
def api_rerun_from_day():
    data = request.json
    start_day = data.get('start_day')
    manual_overrides = data.get('manual_overrides', {})
    
    print(f"Received request to rerun simulation from Day {start_day}.")
    
    if not os.path.exists(MASTER_LOG_FILE):
        return jsonify({"status": "error", "message": "Master log file not found. Run a full simulation first."}), 400
        
    with open(MASTER_LOG_FILE, 'r') as f:
        master_log = json.load(f)
    
    initial_fleet_state_for_rerun = None
    if start_day == 1:
        initialize_fleet_status()
        initial_fleet_state_for_rerun = pd.read_csv("fleet_status.csv")
    else:
        previous_day_log = next((item for item in master_log if item["day"] == start_day - 1), None)
        if previous_day_log:
            initial_fleet_state_for_rerun = pd.DataFrame(previous_day_log['fleet_status_after'])
        else:
            return jsonify({"status": "error", "message": f"Could not find data for Day {start_day - 1} to start rerun."}), 400

    features = ['total_fleet_size', 'target_service_trains', 'avg_fleet_health', 'is_monsoon', 'is_surge']
    targets = ['historical_cost_per_km', 'historical_fatigue_factor', 'historical_branding_penalty', 'historical_target_mileage', 'historical_maint_threshold']

    rerun_log_segment = run_simulation(
        start_day=start_day,
        initial_fleet_state=initial_fleet_state_for_rerun,
        manual_overrides=manual_overrides,
        ai_model=AI_STRATEGIST_MODEL,
        feature_names=features,
        targets=targets
    )
    
    final_log = [item for item in master_log if item['day'] < start_day]
    final_log.extend(rerun_log_segment)

    with open(MASTER_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_log, f, indent=2, default=default_converter, ensure_ascii=False)
        
    print(f"Rerun from Day {start_day} complete. Master log updated.")
    return jsonify({"status": "success", "message": f"Rerun from Day {start_day} complete."})


@app.route('/get_explanations', methods=['GET'])
def api_get_explanations():
    if not os.path.exists(MASTER_LOG_FILE):
        return jsonify({"status": "error", "message": "Master log file not found. Run a simulation first."}), 400

    try:
        with open(MASTER_LOG_FILE, 'r', encoding='utf-8') as f:
            master_log = json.load(f)

        explanations = []
        for entry in master_log:
            if "shap_explanations" in entry and entry.get("shap_explanations"):
                explanations.append({
                    "day": entry["day"], 
                    "shap_explanations": entry["shap_explanations"]
                })
        
        if not explanations:
            return jsonify({"status": "error", "message": "No SHAP explanations found in simulation data."}), 404
            
        return jsonify({"status": "success", "data": explanations})
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return jsonify({"status": "error", "message": f"Corrupted simulation data. Please run a new simulation. Error: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)