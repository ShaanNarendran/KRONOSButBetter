#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 KRONOS - AI Fleet Management System Launcher
# ═══════════════════════════════════════════════════════════════════════════════
# Complete one-command setup and launcher for KRONOS application
# Features: AI Optimization, Fleet Management, SHAP Explanations
# ═══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Unicode symbols
ROCKET="🚀"
GEAR="⚙️"
CHECK="✅"
CROSS="❌"
BRAIN="🧠"
WEB="🌐"
STOP="🛑"
WARNING="⚠️"

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}${ROCKET} KRONOS - AI-POWERED FLEET MANAGEMENT SYSTEM${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}🔹 AI Optimization with OR-Tools${NC}"
echo -e "${CYAN}🔹 Real-time Fleet Management Dashboard${NC}" 
echo -e "${CYAN}🔹 Explainable AI with SHAP Integration${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}${STOP} Shutting down KRONOS...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo -e "${GREEN}${CHECK} Backend stopped${NC}"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo -e "${GREEN}${CHECK} Frontend stopped${NC}"
    fi
    if [ ! -z "$CHATBOT_PID" ]; then
        kill $CHATBOT_PID 2>/dev/null || true
        echo -e "${GREEN}${CHECK} AI Chatbot stopped${NC}"
    fi
    echo -e "${WHITE}👋 KRONOS shutdown complete${NC}"
    exit 0
}

# Set up cleanup trap
trap cleanup EXIT INT TERM

# Validate we're in the correct directory
if [ ! -f "package.json" ] || [ ! -d "backend_v3" ]; then
    echo -e "${RED}${CROSS} Error: Run this script from the KRONOS root directory${NC}"
    echo -e "${RED}   Expected: package.json and backend_v3/ directory${NC}"
    exit 1
fi

echo -e "${YELLOW}${GEAR} Checking environment setup...${NC}"

# Check if virtual environment exists, create if needed
if [ ! -d "/Users/shaannarendran/Downloads/SIHFINAL/.venv" ]; then
    echo -e "${YELLOW}${WARNING} Creating Python virtual environment...${NC}"
    cd /Users/shaannarendran/Downloads/SIHFINAL
    python3 -m venv .venv
    source .venv/bin/activate
    cd KRONOSButBetter
    echo -e "${GREEN}${CHECK} Virtual environment created${NC}"
else
    echo -e "${GREEN}${CHECK} Virtual environment found${NC}"
fi

# Check and install Python dependencies
echo -e "${YELLOW}${GEAR} Installing Python dependencies...${NC}"
/Users/shaannarendran/Downloads/SIHFINAL/.venv/bin/pip install -q flask flask-cors ortools numpy pandas scikit-learn shap joblib python-dotenv google-generativeai
echo -e "${GREEN}${CHECK} Python dependencies installed${NC}"

# Check and install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}${GEAR} Installing Node.js dependencies...${NC}"
    npm install --silent
    echo -e "${GREEN}${CHECK} Node.js dependencies installed${NC}"
else
    echo -e "${GREEN}${CHECK} Node.js dependencies found${NC}"
fi

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"

# Start Backend
echo -e "${BLUE}${BRAIN} Starting AI Backend Engine...${NC}"
echo -e "${CYAN}   🔹 Port: 5001${NC}"
echo -e "${CYAN}   🔹 Features: AI Optimization + SHAP Explanations${NC}"

cd backend_v3
/Users/shaannarendran/Downloads/SIHFINAL/.venv/bin/python backend_run_rerun.py &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo -e "${YELLOW}${GEAR} Initializing AI engine...${NC}"
timeout=30
count=0

while [ $count -lt $timeout ]; do
    if curl -s "http://localhost:5001/get_simulation_data" >/dev/null 2>&1; then
        echo -e "${GREEN}${CHECK} AI Backend ready on http://localhost:5001${NC}"
        break
    fi
    printf "."
    sleep 1
    count=$((count + 1))
    if [ $count -eq $timeout ]; then
        echo -e "\n${RED}${CROSS} Backend failed to start within ${timeout} seconds${NC}"
        exit 1
    fi
done

# Generate chatbot data
echo -e "${YELLOW}${GEAR} Preparing AI chatbot data...${NC}"
cd backend_v3
/Users/shaannarendran/Downloads/SIHFINAL/.venv/bin/python convert_to_chatbot_format.py > /dev/null 2>&1
cd ..
echo -e "${GREEN}${CHECK} Chatbot data ready${NC}"

# Start AI Chatbot Server
echo -e "${BLUE}🤖 Starting AI Chatbot Server...${NC}"
echo -e "${CYAN}   🔹 Port: 5002${NC}"
echo -e "${CYAN}   🔹 Features: RakeAssist AI Co-pilot${NC}"

cd backend_v3
/Users/shaannarendran/Downloads/SIHFINAL/.venv/bin/python chatbot_server.py &
CHATBOT_PID=$!
cd ..

# Wait for chatbot to be ready
echo -e "${YELLOW}${GEAR} Initializing AI chatbot...${NC}"
timeout=15
count=0

while [ $count -lt $timeout ]; do
    if curl -s "http://localhost:5002/ask" -X POST -H "Content-Type: application/json" -d '{"question":"test"}' >/dev/null 2>&1; then
        echo -e "${GREEN}${CHECK} AI Chatbot ready on http://localhost:5002${NC}"
        break
    fi
    printf "."
    sleep 1
    count=$((count + 1))
    if [ $count -eq $timeout ]; then
        echo -e "\n${YELLOW}${WARNING} Chatbot server may need more time to start${NC}"
        break
    fi
done

echo ""

# Start Frontend
echo -e "${BLUE}${WEB} Starting Frontend Dashboard...${NC}"
echo -e "${CYAN}   🔹 Port: 5173${NC}"
echo -e "${CYAN}   🔹 Features: Fleet Management + AI Explanations${NC}"

npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 3

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${CHECK} KRONOS IS NOW RUNNING!${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${WHITE}📱 Access your application:${NC}"
echo -e "${CYAN}   Frontend Dashboard: ${WHITE}http://localhost:5173${NC}"
echo -e "${CYAN}   Backend API:        ${WHITE}http://localhost:5001${NC}"
echo -e "${CYAN}   AI Chatbot API:     ${WHITE}http://localhost:5002${NC}"
echo ""
echo -e "${WHITE}🧠 AI Features Available:${NC}"
echo -e "${CYAN}   🔹 Fleet Management Dashboard${NC}"
echo -e "${CYAN}   🔹 AI Explainability: Menu (≡) → Explainability${NC}"
echo -e "${CYAN}   🔹 RakeAssist AI Chatbot: Menu (≡) → RakeAssist AI${NC}"
echo -e "${CYAN}   🔹 Real-time Fleet Optimization${NC}"
echo -e "${CYAN}   🔹 SHAP Decision Analysis${NC}"
echo ""
echo -e "${WHITE}💡 Usage Tips:${NC}"
echo -e "${CYAN}   • View fleet status and maintenance schedules${NC}"
echo -e "${CYAN}   • Run simulations to see AI optimization in action${NC}"
echo -e "${CYAN}   • Click 'Explainability' to see AI decision reasoning${NC}"
echo -e "${CYAN}   • Use 'RakeAssist AI' to chat about train assignments${NC}"
echo -e "${CYAN}   • SHAP values show which factors influenced AI choices${NC}"
echo ""
echo -e "${YELLOW}To stop KRONOS, press Ctrl+C${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════════════════════${NC}"

# Keep the script running and wait for user to stop
wait