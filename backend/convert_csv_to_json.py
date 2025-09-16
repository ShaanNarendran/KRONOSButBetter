import pandas as pd
import json
import os

def convert_csv_to_json():
    # Get the absolute path to the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute paths for the input CSV and output JSON files
    csv_file_path = os.path.join(script_dir, 'data', 'monthly_simulation_log.csv')
    json_file_path = os.path.join(script_dir, 'data', 'simulation_log.json')

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    records = df.to_dict(orient='records')

    # Group records by simulation_day
    grouped_by_day = {}
    for record in records:
        day = record['simulation_day']
        if day not in grouped_by_day:
            grouped_by_day[day] = []
        grouped_by_day[day].append(record)

    # Create the final JSON structure
    simulation_log = []
    for day, fleet_status in grouped_by_day.items():
        # Determine the plan for the day (example logic, you might need to adjust)
        service_count = sum(1 for r in fleet_status if r['status'] == 'SERVICE')
        maintenance_count = sum(1 for r in fleet_status if r['status'] == 'MAINTENANCE')
        
        plan = {
            "day": int(day),
            "plan": {
                "SERVICE": [r['train_id'] for r in fleet_status if r['status'] == 'SERVICE'],
                "MAINTENANCE": [r['train_id'] for r in fleet_status if r['status'] == 'MAINTENANCE'],
                "STANDBY": [r['train_id'] for r in fleet_status if r['status'] == 'STANDBY']
            },
            "fleet_status_today": fleet_status
        }
        simulation_log.append(plan)

    # Sort the log by day
    simulation_log.sort(key=lambda x: x['day'])

    # Write to JSON file
    with open(json_file_path, 'w') as f:
        json.dump(simulation_log, f, indent=4)

    print(f"Successfully converted {csv_file_path} to {json_file_path}")

if __name__ == '__main__':
    convert_csv_to_json()
