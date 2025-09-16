#!/bin/bash

# KRONOS Quick Start Script
echo "🚀 Starting KRONOS Application..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the KRONOS project root directory"
    exit 1
fi

# Check if setup has been run
if [ ! -d "backend/venv" ] || [ ! -f "backend/.env" ]; then
    echo "⚠️  Initial setup required. Running setup-dev.sh..."
    ./setup-dev.sh
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed. Please resolve issues and try again."
        exit 1
    fi
fi

# Backend setup
echo "🔧 Setting up backend..."
cd backend

# Activate virtual environment
echo "   Activating Python virtual environment..."
source venv/bin/activate

# Generate fresh data
echo "   Running optimization simulation..."
python new_solver.py

echo "   Converting data for frontend..."
python convert_csv_to_json.py

echo "   Copying data to frontend..."
cp data/simulation_log.json ../public/

echo "   Starting API server..."
python api_server.py &
API_PID=$!

cd ..

# Frontend setup
echo "🌐 Starting frontend development server..."
npm run dev &
FRONTEND_PID=$!

# Wait a moment for servers to start
sleep 3

echo ""
echo "🎉 KRONOS is now running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "   All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait

echo "--- Backend Data Generation Complete ---"

# Step 6: Start the chatbot API server in the background
echo ">>> Starting the Chatbot API server in the background..."
echo "    The server will run on port 5001."
nohup python backend/api_server.py &

echo "--- All backend processes are running. You can now start the frontend. ---"
