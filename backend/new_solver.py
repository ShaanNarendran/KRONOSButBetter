import pandas as pd
from datetime import datetime, timedelta
from ortools.sat.python import cp_model
import sys
import time

# --- 1. SIMULATION CONFIGURATION ---
SIMULATION_START_DATE = datetime(2025, 9, 1)
SIMULATION_MONTH_DAYS = 30
DAILY_KM_PER_TRAIN = 200
DAILY_HOURS_PER_TRAIN = 16
HEALTH_SCORE_MAINTENANCE_THRESHOLD = 50
FATIGUE_PENALTY_FACTOR = 500
BOGIE_SERVICE_INTERVAL_KM = 25000
CERTIFICATE_VALIDITY_DAYS = 365
# NEW: An escalating penalty for expired certificates
PENALTY_PER_EXPIRED_DAY = 5 # Health score drops by 5 points for each day expired

# Ad-hoc supervisor inputs for specific days
MANUAL_INPUTS_CALENDAR = {
    5: {
        "Rake-12": {"health_penalty": 40, "reason": "Visual inspection shows damaged pantograph"}
    },
    10: {
        "Rake-08": {"health_penalty": 15, "reason": "Minor graffiti on exterior panel reported"}
    },
    15: {
        "Rake-19": {"force_maintenance": True, "reason": "Driver reported unusual noise from bogie"}
    },
    20: {
        "Rake-04": {"health_penalty": 25, "reason": "Faulty door sensor reported"},
        "Rake-16": {"force_maintenance": True, "reason": "Leak in HVAC unit"}
    },
    25: {
        "Rake-01": {"force_maintenance": True, "reason": "Sudden failure of passenger information display"}
    }
}
MONTHLY_SCENARIOS = ['NORMAL'] * SIMULATION_MONTH_DAYS
MONTHLY_SCENARIOS[6] = MONTHLY_SCENARIOS[7] = 'FESTIVAL_SURGE'
MONTHLY_SCENARIOS[12] = MONTHLY_SCENARIOS[13] = 'HEAVY_MONSOON'
MONTHLY_SCENARIOS[21] = 'FESTIVAL_SURGE'

# --- 2. COSTS AND MODIFIERS ---
BASE_COSTS = {"PER_KM_DEVIATION": 5, "BRANDING_SLA_PENALTY": 50000, "PER_SHUNT": 500}
MAINTENANCE_SLOT_PENALTY = 1000000
SERVICE_SHORTFALL_PENALTY = 5000000
SCENARIO_MODIFIERS = {
    "NORMAL": {"MIN_SERVICE": 6, "MAX_SERVICE": 6, "MAINTENANCE_SLOTS": 2},
    "HEAVY_MONSOON": {"MIN_SERVICE": 6, "MAX_SERVICE": 6, "MAINTENANCE_SLOTS": 2, "WEATHER_PENALTY_OLD_BRAKES": 15000, "WEATHER_PENALTY_BOGIE_WEAR": 20000},
    "FESTIVAL_SURGE": {"MIN_SERVICE": 6, "MAX_SERVICE": 6, "MAINTENANCE_SLOTS": 1}
}

# --- 3. HELPER FUNCTIONS ---
def get_fleet_data(file_path="data/fleet_status.csv"):
    try: return pd.read_csv(file_path)
    except FileNotFoundError: print(f"Error: '{file_path}' not found. Please run initialize_month.py first."); return None

def preprocess_and_health_score(df, current_day, manual_inputs):
    df['cert_telecom_expiry'] = pd.to_datetime(df['cert_telecom_expiry'])
    today = SIMULATION_START_DATE + timedelta(days=current_day - 1)
    df['is_cert_expired'] = df['cert_telecom_expiry'] < today
    
    # Health score calculation
    df['health_score'] = 100.0
    df['km_since_last_service'] = df['current_km'] - df['bogie_last_service_km']
    df['health_score'] -= (df['km_since_last_service'] / 200).astype(float)
    if 'consecutive_service_days' in df.columns:
        df['health_score'] -= df['consecutive_service_days']
    
    # --- NEW: URGENCY PENALTY FOR EXPIRED CERTIFICATES ---
    expired_trains = df[df['is_cert_expired']].index
    days_expired = (today - df.loc[expired_trains, 'cert_telecom_expiry']).dt.days
    expired_penalty = days_expired * PENALTY_PER_EXPIRED_DAY
    df.loc[expired_trains, 'health_score'] -= expired_penalty

    priority_penalties = {'LOW': 10, 'MEDIUM': 20, 'CRITICAL': 50}
    for p, penalty in priority_penalties.items():
        df.loc[(df['job_card_status'] == 'OPEN') & (df['job_card_priority'] == p), 'health_score'] -= penalty
        
    df['manual_force_maintenance'] = False
    for train_id, override in manual_inputs.items():
        if 'health_penalty' in override: df.loc[df['train_id'] == train_id, 'health_score'] -= override['health_penalty']
        if 'force_maintenance' in override: df.loc[df['train_id'] == train_id, 'manual_force_maintenance'] = True
    df['health_score'] = df['health_score'].clip(lower=0)
    return df

# --- 4. THE OPTIMIZER ---
def solve_daily_optimization(fleet_df, current_day, scenario="NORMAL"):

    model = cp_model.CpModel()
    modifiers = SCENARIO_MODIFIERS[scenario]
    is_in_service = {r['train_id']: model.NewBoolVar(f"s_{r['train_id']}") for _, r in fleet_df.iterrows()}
    is_in_maintenance = {r['train_id']: model.NewBoolVar(f"m_{r['train_id']}") for _, r in fleet_df.iterrows()}
    is_on_standby = {r['train_id']: model.NewBoolVar(f"b_{r['train_id']}") for _, r in fleet_df.iterrows()}
    for _, row in fleet_df.iterrows():
        tid = row['train_id']
        model.Add(is_in_service[tid] + is_in_maintenance[tid] + is_on_standby[tid] == 1)
        if row['is_cert_expired'] or row['job_card_priority'] == 'CRITICAL': model.Add(is_in_service[tid] == 0)
        if row['health_score'] < HEALTH_SCORE_MAINTENANCE_THRESHOLD or row['manual_force_maintenance']:
            model.Add(is_in_maintenance[tid] == 1)
    model.Add(sum(is_in_service.values()) <= modifiers['MAX_SERVICE'])
    total_objective = []
    num_in_service = sum(is_in_service.values())
    shortfall = model.NewIntVar(0, modifiers['MIN_SERVICE'], 'shortfall')
    model.Add(shortfall >= modifiers['MIN_SERVICE'] - num_in_service)
    total_objective.append(shortfall * SERVICE_SHORTFALL_PENALTY)
    num_in_maint = sum(is_in_maintenance.values())
    maint_dev = model.NewIntVar(-len(fleet_df), len(fleet_df), 'maint_dev')
    model.Add(maint_dev == num_in_maint - modifiers['MAINTENANCE_SLOTS'])
    abs_maint_dev = model.NewIntVar(0, len(fleet_df), 'abs_maint_dev')
    model.AddAbsEquality(abs_maint_dev, maint_dev)
    total_objective.append(abs_maint_dev * MAINTENANCE_SLOT_PENALTY)
    for _, row in fleet_df.iterrows():
        
        tid, service_var = row['train_id'], is_in_service[row['train_id']]
        consecutive_days = row.get('consecutive_service_days', 0)
        fatigue_cost = int((consecutive_days**2) * FATIGUE_PENALTY_FACTOR)
        service_cost = fatigue_cost
        monthly_target_km = DAILY_KM_PER_TRAIN * 22
        ideal_km = (monthly_target_km / SIMULATION_MONTH_DAYS) * current_day
        urgency_multiplier = current_day / SIMULATION_MONTH_DAYS
        mileage_cost = int(abs(row['current_km'] - ideal_km) * BASE_COSTS["PER_KM_DEVIATION"] * urgency_multiplier)
        service_cost += mileage_cost
        service_cost += int(row['stabling_shunt_moves'] * BASE_COSTS["PER_SHUNT"])
        if scenario == "HEAVY_MONSOON":
            if row['brake_model'] == 'HydroMech_v1': service_cost += modifiers['WEATHER_PENALTY_OLD_BRAKES']
            if row['km_since_last_service'] > BOGIE_SERVICE_INTERVAL_KM: service_cost += modifiers['WEATHER_PENALTY_BOGIE_WEAR']
        total_objective.append(service_cost * service_var)
        total_objective.append(int(row['health_score']) * is_in_maintenance[tid])
        
        if row['branding_sla_active']:
            hours_needed = row['target_hours'] - row['current_hours']
            if hours_needed > 0:
                run_rate = hours_needed / (SIMULATION_MONTH_DAYS - current_day + 1)
                urgency = run_rate / DAILY_HOURS_PER_TRAIN
                penalty = int(BASE_COSTS["BRANDING_SLA_PENALTY"] * urgency)
                total_objective.append(penalty * (1 - service_var))
    model.Minimize(sum(total_objective))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        plan = {'SERVICE': [], 'MAINTENANCE': [], 'STANDBY': []}
        for _, r in fleet_df.iterrows():
            if solver.Value(is_in_service[r['train_id']]): plan['SERVICE'].append(r['train_id'])
            elif solver.Value(is_in_maintenance[r['train_id']]): plan['MAINTENANCE'].append(r['train_id'])
            else: plan['STANDBY'].append(r['train_id'])
        return plan, int(solver.ObjectiveValue())
    return None, None

# --- 5. SIMULATION ENGINE ---
def apply_daily_updates(df, plan, current_day):

    service_trains = plan['SERVICE']
    maintenance_trains = plan['MAINTENANCE']
    today = SIMULATION_START_DATE + timedelta(days=current_day - 1)
    if 'consecutive_service_days' not in df.columns: df['consecutive_service_days'] = 0
    df.loc[df['train_id'].isin(service_trains), 'consecutive_service_days'] += 1
    df.loc[~df['train_id'].isin(service_trains), 'consecutive_service_days'] = 0
    df.loc[df['train_id'].isin(service_trains), 'current_km'] += DAILY_KM_PER_TRAIN
    branded_service = df[(df['train_id'].isin(service_trains)) & (df['branding_sla_active'])]
    df.loc[df.index.isin(branded_service.index), 'current_hours'] += DAILY_HOURS_PER_TRAIN
    for train_id in maintenance_trains:
        train_index = df[df['train_id'] == train_id].index
        current_expiry = pd.to_datetime(df.loc[train_index, 'cert_telecom_expiry'].iloc[0])
        if current_expiry < today:
            new_expiry_date = today + timedelta(days=CERTIFICATE_VALIDITY_DAYS)
            df.loc[train_index, 'cert_telecom_expiry'] = new_expiry_date
            print(f"    INFO: Certificate for {train_id} renewed to {new_expiry_date.strftime('%Y-%m-%d')}")
    df.loc[df['train_id'].isin(maintenance_trains), 'health_score'] = 100
    df.loc[df['train_id'].isin(maintenance_trains), 'bogie_last_service_km'] = df.loc[df['train_id'].isin(maintenance_trains), 'current_km']
    if 'total_service_days_month' not in df.columns: df['total_service_days_month'] = 0
    if 'total_maintenance_days_month' not in df.columns: df['total_maintenance_days_month'] = 0
    df.loc[df['train_id'].isin(service_trains), 'total_service_days_month'] += 1
    df.loc[df['train_id'].isin(maintenance_trains), 'total_maintenance_days_month'] += 1
    return df

# --- 6. MAIN SIMULATION LOOP ---
if __name__ == "__main__":
    # Initialize monthly simulation log
    monthly_log = []

    for day in range(1, SIMULATION_MONTH_DAYS + 1):
        scenario = MONTHLY_SCENARIOS[day - 1]
        manual_inputs_today = MANUAL_INPUTS_CALENDAR.get(day, {})
        print(f"\n{'='*25} DAY {day} | SCENARIO: {scenario.replace('_', ' ')} {'='*25}")
        if manual_inputs_today: print(f"MANUAL OVERRIDES FOR TODAY: {manual_inputs_today}")
        fleet_df = get_fleet_data()
        if fleet_df is None: break
        fleet_df = preprocess_and_health_score(fleet_df, day, manual_inputs_today)
        daily_plan, daily_cost = solve_daily_optimization(fleet_df, day, scenario)
        if daily_plan:
            print("Optimal plan generated for tomorrow:")
            if daily_cost is not None:
                true_operational_cost = daily_cost % MAINTENANCE_SLOT_PENALTY
                print(f"  - Projected Operational Cost for Day {day+1}: ₹{true_operational_cost:,}")
            for category, trains in daily_plan.items():
                print(f"  - {category} ({len(trains)}): {sorted(trains)}")
            
            updated_df = apply_daily_updates(fleet_df, daily_plan, day)
            
            # Log daily plan and fleet status for monthly simulation log
            for _, row in updated_df.iterrows():
                train_id = row['train_id']
                if train_id in daily_plan['SERVICE']:
                    status = 'SERVICE'
                elif train_id in daily_plan['MAINTENANCE']:
                    status = 'MAINTENANCE'
                else:
                    status = 'STANDBY'
                
                log_entry = row.to_dict()
                log_entry['simulation_day'] = day
                log_entry['status'] = status
                monthly_log.append(log_entry)
            
            updated_df.to_csv("data/fleet_status.csv", index=False)
        else:
            print(f"CRITICAL FAILURE on Day {day}. Could not generate a plan. Halting simulation.")
            break
        time.sleep(0.5)
    print(f"\n{'='*25} END OF MONTH SIMULATION COMPLETE {'='*25}")
    
    # Save monthly simulation log to CSV
    if monthly_log:
        monthly_log_df = pd.DataFrame(monthly_log)
        monthly_log_df.to_csv("data/monthly_simulation_log.csv", index=False)
        print(f"Monthly simulation log saved to data/monthly_simulation_log.csv")
    
    final_df = get_fleet_data()
    if final_df is not None:
        print("\n--- FINAL FLEET STATUS AT END OF MONTH ---")
        columns_to_show = ['train_id', 'health_score', 'current_km', 'current_hours', 'consecutive_service_days', 'total_service_days_month', 'total_maintenance_days_month', 'cert_telecom_expiry']
        final_df['cert_telecom_expiry'] = pd.to_datetime(final_df['cert_telecom_expiry']).dt.strftime('%Y-%m-%d')
        print(final_df[columns_to_show].to_string(index=False))