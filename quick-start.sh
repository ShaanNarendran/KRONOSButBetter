#!/bin/bash

# KRONOS Quick Start Script - Just start the servers
echo "🚀 Quick Starting KRONOS..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the KRONOS project root directory"
    exit 1
fi

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Initial setup required. Run './setup-dev.sh' first"
    exit 1
fi

# Backend setup
echo "🔧 Starting backend services..."
cd backend

# Activate virtual environment
source venv/bin/activate

# Start API server
echo "   Starting API server..."
python api_server.py &
API_PID=$!

cd ..

# Frontend setup
echo "🌐 Starting frontend..."
npm run dev &
FRONTEND_PID=$!

# Wait for servers to start
sleep 3

echo ""
echo "🎉 KRONOS is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:5000"
echo ""
echo "💡 For fresh data, run './run_all.sh' instead"
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "   Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM
wait