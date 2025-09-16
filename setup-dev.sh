#!/bin/bash

# Development setup script for KRONOS
# Sets up the development environment from scratch

echo "🛠️  KRONOS Development Setup"
echo "============================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking system requirements..."

if ! command_exists python3; then
    echo "❌ Python 3.8+ is required"
    echo "   Install from: https://python.org/downloads/"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js 16+ is required"
    echo "   Install from: https://nodejs.org/"
    exit 1
fi

if ! command_exists git; then
    echo "❌ Git is required"
    echo "   Install from: https://git-scm.com/"
    exit 1
fi

echo "✅ System requirements satisfied"

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
cd backend

if [ -d "venv" ]; then
    echo "   Virtual environment already exists"
else
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

echo "   Activating virtual environment..."
source venv/bin/activate

echo "   Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Setup Node.js environment
echo "📦 Setting up Node.js environment..."
if [ -d "node_modules" ]; then
    echo "   Dependencies already installed"
else
    echo "   Installing Node.js dependencies..."
    npm install
fi

# Check for environment file
echo "🔧 Checking environment configuration..."
if [ -f "backend/.env" ]; then
    echo "   Environment file exists"
else
    echo "   Creating sample environment file..."
    cat > backend/.env << EOF
# KRONOS Backend Environment Variables
# Copy this file and add your actual API keys

# Google Gemini AI API Key (required for chatbot)
GEMINI_API_KEY=your_google_gemini_api_key_here

# Development settings
DEBUG=true
EOF
    echo "   ⚠️  Please edit backend/.env with your actual API keys"
fi

# Initialize data
echo "📊 Initializing system data..."
cd backend
source venv/bin/activate

echo "   Training AI models..."
python train_weight_predictor.py

echo "   Initializing fleet data..."
python initialize_month.py

echo "   Running optimization simulation..."
python new_solver.py

echo "   Converting data for frontend..."
python convert_csv_to_json.py

echo "   Copying data to frontend..."
cp data/simulation_log.json ../public/

cd ..

# Final checks
echo "🔍 Running system validation..."

# Check if all required files exist
required_files=(
    "backend/data/fleet_status.csv"
    "backend/data/simulation_log.json"
    "backend/models/strategy_model.joblib"
    "public/simulation_log.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done

echo ""
echo "🎉 Development setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Run './start.sh' to start the application"
echo "3. Visit http://localhost:5173 to see the application"
echo ""
echo "For development:"
echo "- Backend: cd backend && source venv/bin/activate && python api_server.py"
echo "- Frontend: npm run dev"
echo ""