#!/bin/bash

# KRONOS Application Runner - Clean & Simple
# Runs the complete KRONOSv3 application with AI explanations

set -e  # Exit on any error

echo "🚀 KRONOS - AI-Powered Fleet Management System"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "backend_v3" ]; then
    echo "❌ Error: Run this script from the KRONOS app root directory"
    echo "   Expected: package.json and backend_v3/ directory"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down KRONOS..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "   ✅ Backend stopped"
    fi
    echo "👋 KRONOS application stopped cleanly"
}

# Set up cleanup trap
trap cleanup EXIT INT TERM

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Installing Python dependencies..."
    pip install flask flask-cors ortools numpy pandas scikit-learn shap
else
    source .venv/bin/activate
fi

# Check if node modules exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start backend in background
echo ""
echo "🔧 Starting KRONOSv3 Backend..."
echo "   Port: 5001"
echo "   Features: AI Optimization + SHAP Explanations"

cd backend_v3
python backend_run_rerun.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start with timeout
echo "⏳ Waiting for backend to initialize..."
timeout=30
count=0

while [ $count -lt $timeout ]; do
    if curl -s "http://localhost:5001/get_simulation_data" >/dev/null 2>&1; then
        echo "✅ Backend ready on http://localhost:5001"
        break
    fi
    sleep 1
    count=$((count + 1))
    if [ $count -eq $timeout ]; then
        echo "❌ Backend failed to start within ${timeout} seconds"
        exit 1
    fi
done

# Start frontend
echo ""
echo "🎨 Starting Frontend Dashboard..."
echo "   Port: 5174 (or next available)"
echo "   Features: Fleet Management + AI Explanations"
echo ""
echo "📱 Access your app at: http://localhost:5174"
echo "🧠 AI Explanations: Menu (≡) → Explainability"
echo ""
echo "💡 Tips:"
echo "   • View fleet status and maintenance schedules"
echo "   • Click 'Explainability' to see AI decision reasoning"
echo "   • SHAP values show which factors influenced AI choices"
echo ""
echo "To stop the application, press Ctrl+C"
echo "=========================================="

# Start frontend (this will block until user stops)
npm run dev