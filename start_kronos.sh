#!/bin/bash

# KRONOS Complete Startup Script
echo "🚀 Starting KRONOS Application..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Run this script from the KRONOS app root directory"
    exit 1
fi

# Start backend in background
echo "🔧 Starting Flask Backend..."
cd backend_v3
/Users/shaannarendran/Downloads/KRONOS-KRONOS_app/.venv/bin/python backend_run_rerun.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if curl -s "http://localhost:5001/get_simulation_data" >/dev/null 2>&1; then
    echo "✅ Backend started successfully on http://localhost:5001"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🎨 Starting Frontend..."
echo "📱 Frontend will be available at http://localhost:5174"
echo "🧠 AI Explanations available via menu → Explainability"
echo ""
echo "To stop both servers, press Ctrl+C"

# Start frontend (this will block)
npm run dev

# Cleanup: Kill backend when frontend stops
echo "🛑 Stopping backend..."
kill $BACKEND_PID 2>/dev/null
echo "👋 KRONOS application stopped"