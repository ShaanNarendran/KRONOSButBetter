import json
import pandas as pd
import os

def convert_json_to_csv():
    """Convert simulation_log_master.json to monthly_simulation_log.csv format for chatbot"""
    
    # Input and output paths
    json_file = "simulation_log_master.json"
    csv_file = "monthly_simulation_log.csv"
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return
    
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to the format expected by the chatbot
    rows = []
    
    for day_entry in data:
        day = day_entry['day']
        scenario = day_entry.get('scenario', 'NORMAL')
        
        # Get the plan assignments
        plan = day_entry.get('plan', {})
        
        # Get fleet status after (which contains health scores)
        fleet_status = day_entry.get('fleet_status_after', [])
        
        # Create a lookup for health scores
        health_lookup = {}
        for train in fleet_status:
            train_id = train.get('train_id', '')
            health_lookup[train_id] = train.get('health_score', 0)
        
        # Process each assignment category
        for status, train_ids in plan.items():
            if isinstance(train_ids, list):
                for train_id in train_ids:
                    # Calculate consecutive service days (simplified)
                    consecutive_days = 0
                    if status == 'SERVICE':
                        # Look back through previous days to count consecutive service
                        for prev_day in range(max(1, day-10), day):
                            prev_entry = next((d for d in data if d['day'] == prev_day), None)
                            if prev_entry and train_id in prev_entry.get('plan', {}).get('SERVICE', []):
                                consecutive_days += 1
                            else:
                                break
                    
                    row = {
                        'simulation_day': day,
                        'train_id': train_id,
                        'status': status,
                        'health_score': health_lookup.get(train_id, 100),
                        'consecutive_service_days': consecutive_days,
                        'scenario': scenario
                    }
                    rows.append(row)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Converted {json_file} to {csv_file}")
    print(f"📊 Generated {len(rows)} records for {len(df['simulation_day'].unique())} days")
    print(f"🚂 Covering {len(df['train_id'].unique())} unique trains")

if __name__ == "__main__":
    convert_json_to_csv()