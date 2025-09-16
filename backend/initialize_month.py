import pandas as pd
import os

def initialize_fleet_status(base_file="data/fleet_data.csv", output_file="data/fleet_status.csv"):
    """
    Creates the starting CSV file for a new month from the master data.
    Resets all monthly tracking columns to their initial state.
    """
    try:
        script_dir = os.path.dirname(__file__)
        base_file_path = os.path.join(script_dir, base_file)
        output_file_path = os.path.join(script_dir, output_file)
        base_df = pd.read_csv(base_file_path)
    except FileNotFoundError:
        print(f"Error: Base data file '{base_file_path}' not found. Please ensure it exists.")
        return

    # Add/reset columns for the start of the month
    base_df['health_score'] = 100
    base_df['current_km'] = 0
    base_df['current_hours'] = 0.0 # Use float for hours
    base_df['job_card_status'] = 'CLOSED'
    base_df['job_card_priority'] = 'NONE'
    base_df['bogie_last_service_km'] = 0
    base_df['consecutive_service_days'] = 0
    
    # Add summary statistic columns
    base_df['total_service_days_month'] = 0
    base_df['total_maintenance_days_month'] = 0
    
    # Fill NaN values in branding columns to prevent errors
    base_df[['target_hours', 'current_hours']] = base_df[['target_hours', 'current_hours']].fillna(0)

    final_df = base_df.copy()
    final_df.to_csv(output_file_path, index=False)
    print(f"Fleet status initialized with monthly stats tracking in '{output_file_path}'")

if __name__ == "__main__":
    initialize_fleet_status()

