#!/bin/bash

# Setup script for running the new KRONOSv3 backend
echo "Setting up KRONOSv3 backend..."

# Check if we're in the correct directory
if [ ! -f "package.json" ]; then
    echo "Error: This script should be run from the KRONOS app root directory"
    exit 1
fi

# Create backend directory structure to match KRONOSv3
mkdir -p backend_v3
cd backend_v3

echo "Downloading KRONOSv3 backend files..."

# Download the main files from KRONOSv3 repository
curl -o answer_final.py "https://raw.githubusercontent.com/VishnuM049/KRONOSv3/main/answer_final.py"
curl -o backend_run_rerun.py "https://raw.githubusercontent.com/VishnuM049/KRONOSv3/main/backend_run_rerun.py" 
curl -o brain_make.py "https://raw.githubusercontent.com/VishnuM049/KRONOSv3/main/brain_make.py"
curl -o fleet_data.csv "https://raw.githubusercontent.com/VishnuM049/KRONOSv3/main/fleet_data.csv"
curl -o historical_data_retrain.csv "https://raw.githubusercontent.com/VishnuM049/KRONOSv3/main/historical_data_retrain.csv"

echo "Installing Python dependencies..."

# Install required Python packages
pip3 install pandas flask ortools scikit-learn joblib shap numpy

echo "Training the AI model..."

# Train the model first
python3 brain_make.py

echo "Starting the Flask backend server..."

# Start the backend server
python3 backend_run_rerun.py

echo "Backend is now running on http://localhost:5000"
echo "Your frontend should now be able to connect to the new backend!"