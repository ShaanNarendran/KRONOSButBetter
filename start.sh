#!/bin/bash

# Quick start script for KRONOS application
# This script provides a simple way to start both backend and frontend

echo "🚇 KRONOS Quick Start"
echo "===================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the KRONOS-KRONOS_app root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Check if backend dependencies are installed
if [ ! -f "backend/venv/lib/python*/site-packages/ortools*" ]; then
    echo "🐍 Installing backend dependencies..."
    cd backend
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found"
    echo "   Please create backend/.env with your GEMINI_API_KEY"
    echo "   Example: GEMINI_API_KEY=your_api_key_here"
    echo ""
fi

# Run the full setup
echo "🚀 Starting KRONOS backend setup..."
./run_all.sh

# Start frontend in the background
echo "🎨 Starting frontend development server..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ KRONOS is starting up!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
trap "echo '🛑 Stopping services...'; kill $FRONTEND_PID 2>/dev/null; pkill -f 'python.*api_server.py' 2>/dev/null; exit 0" INT

# Keep script running
wait $FRONTEND_PID