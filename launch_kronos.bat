@echo off
setlocal EnableDelayedExpansion

REM ═══════════════════════════════════════════════════════════════════════════════
REM 🚀 KRONOS - AI Fleet Management System Launcher (Windows)
REM ═══════════════════════════════════════════════════════════════════════════════
REM Complete one-command setup and launcher for KRONOS application
REM Features: AI Optimization, Fleet Management, SHAP Explanations
REM ═══════════════════════════════════════════════════════════════════════════════

REM Unicode symbols and colors for Windows
set "ROCKET=🚀"
set "GEAR=⚙️"
set "CHECK=✅"
set "CROSS=❌"
set "BRAIN=🧠"
set "WEB=🌐"
set "STOP=🛑"
set "WARNING=⚠️"

echo ═══════════════════════════════════════════════════════════════════════════════
echo %ROCKET% KRONOS - AI-POWERED FLEET MANAGEMENT SYSTEM
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🔹 AI Optimization with OR-Tools
echo 🔹 Real-time Fleet Management Dashboard
echo 🔹 Explainable AI with SHAP Integration
echo ═══════════════════════════════════════════════════════════════════════════════

REM Set up cleanup handler
set "BACKEND_PID="
set "FRONTEND_PID="
set "CHATBOT_PID="

REM Validate we're in the correct directory
if not exist "package.json" (
    echo %CROSS% Error: Run this script from the KRONOS root directory
    echo    Expected: package.json and backend_v3\ directory
    pause
    exit /b 1
)

if not exist "backend_v3" (
    echo %CROSS% Error: Run this script from the KRONOS root directory
    echo    Expected: package.json and backend_v3\ directory
    pause
    exit /b 1
)

echo %GEAR% Checking environment setup...

REM Get the current directory for virtual environment path
set "CURRENT_DIR=%CD%"
set "VENV_PATH=%CURRENT_DIR%\.venv"

REM Check if virtual environment exists, create if needed
if not exist "%VENV_PATH%" (
    echo %WARNING% Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo %CROSS% Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
    echo %CHECK% Virtual environment created
) else (
    echo %CHECK% Virtual environment found
)

REM Activate virtual environment and install dependencies
echo %GEAR% Installing Python dependencies...
call "%VENV_PATH%\Scripts\activate.bat"
if errorlevel 1 (
    echo %CROSS% Failed to activate virtual environment
    pause
    exit /b 1
)

pip install -q flask flask-cors ortools numpy pandas scikit-learn shap joblib python-dotenv google-generativeai
if errorlevel 1 (
    echo %CROSS% Failed to install Python dependencies
    pause
    exit /b 1
)
echo %CHECK% Python dependencies installed

REM Check and install Node.js dependencies
if not exist "node_modules" (
    echo %GEAR% Installing Node.js dependencies...
    call npm install --silent
    if errorlevel 1 (
        echo %CROSS% Failed to install Node.js dependencies. Make sure Node.js is installed.
        pause
        exit /b 1
    )
    echo %CHECK% Node.js dependencies installed
) else (
    echo %CHECK% Node.js dependencies found
)

echo ═══════════════════════════════════════════════════════════════════════════════

REM Start Backend
echo %BRAIN% Starting AI Backend Engine...
echo    🔹 Port: 5001
echo    🔹 Features: AI Optimization + SHAP Explanations

cd backend_v3
start "KRONOS Backend" /min "%VENV_PATH%\Scripts\python.exe" backend_run_rerun.py
cd ..

REM Wait for backend to be ready
echo %GEAR% Initializing AI engine...
set /a timeout=30
set /a count=0

:wait_backend
if !count! geq !timeout! (
    echo.
    echo %CROSS% Backend failed to start within !timeout! seconds
    pause
    exit /b 1
)

REM Check if backend is ready using curl or powershell
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:5001/get_simulation_data' -Method Get -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo|set /p="."
    timeout /t 1 /nobreak >nul
    set /a count+=1
    goto wait_backend
)

echo.
echo %CHECK% AI Backend ready on http://localhost:5001

REM Generate chatbot data
echo %GEAR% Preparing AI chatbot data...
cd backend_v3
"%VENV_PATH%\Scripts\python.exe" convert_to_chatbot_format.py >nul 2>&1
cd ..
echo %CHECK% Chatbot data ready

REM Start AI Chatbot Server
echo 🤖 Starting AI Chatbot Server...
echo    🔹 Port: 5002
echo    🔹 Features: RakeAssist AI Co-pilot

cd backend_v3
start "KRONOS Chatbot" /min "%VENV_PATH%\Scripts\python.exe" chatbot_server.py
cd ..

REM Wait for chatbot to be ready
echo %GEAR% Initializing AI chatbot...
set /a timeout=15
set /a count=0

:wait_chatbot
if !count! geq !timeout! (
    echo.
    echo %WARNING% Chatbot server may need more time to start
    goto start_frontend
)

REM Check if chatbot is ready
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:5002/ask' -Method Post -ContentType 'application/json' -Body '{\"question\":\"test\"}' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo|set /p="."
    timeout /t 1 /nobreak >nul
    set /a count+=1
    goto wait_chatbot
)

echo.
echo %CHECK% AI Chatbot ready on http://localhost:5002

:start_frontend
echo.

REM Start Frontend
echo %WEB% Starting Frontend Dashboard...
echo    🔹 Port: 5173
echo    🔹 Features: Fleet Management + AI Explanations

start "KRONOS Frontend" /min npm run dev

REM Wait a moment for frontend to start
timeout /t 3 /nobreak >nul

echo ═══════════════════════════════════════════════════════════════════════════════
echo %CHECK% KRONOS IS NOW RUNNING!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📱 Access your application:
echo    Frontend Dashboard: http://localhost:5173
echo    Backend API:        http://localhost:5001
echo    AI Chatbot API:     http://localhost:5002
echo.
echo 🧠 AI Features Available:
echo    🔹 Fleet Management Dashboard
echo    🔹 AI Explainability: Menu (≡) → Explainability
echo    🔹 RakeAssist AI Chatbot: Menu (≡) → RakeAssist AI
echo    🔹 Real-time Fleet Optimization
echo    🔹 SHAP Decision Analysis
echo.
echo 💡 Usage Tips:
echo    • View fleet status and maintenance schedules
echo    • Run simulations to see AI optimization in action
echo    • Click 'Explainability' to see AI decision reasoning
echo    • Use 'RakeAssist AI' to chat about train assignments
echo    • SHAP values show which factors influenced AI choices
echo.
echo To stop KRONOS, close this window or press Ctrl+C
echo ═══════════════════════════════════════════════════════════════════════════════

REM Open the application in default browser
timeout /t 2 /nobreak >nul
start http://localhost:5173

REM Keep the script running
echo.
echo Press any key to stop all KRONOS services...
pause >nul

REM Cleanup - kill all KRONOS processes
echo.
echo %STOP% Shutting down KRONOS...
taskkill /f /fi "WindowTitle eq KRONOS Backend*" >nul 2>&1
taskkill /f /fi "WindowTitle eq KRONOS Frontend*" >nul 2>&1
taskkill /f /fi "WindowTitle eq KRONOS Chatbot*" >nul 2>&1
echo %CHECK% All KRONOS services stopped
echo 👋 KRONOS shutdown complete
pause