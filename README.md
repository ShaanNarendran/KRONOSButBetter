# KRONOS Intelligent Fleet Management System# KRONOS Train Set Optimization System# React + Vite

> Advanced AI-powered train fleet optimization and management platform

![KRONOS Logo](https://img.shields.io/badge/KRONOS-Fleet%20Management-blue?style=for-the-badge)A comprehensive train fleet management and optimization system for metro operations, featuring AI-powered scheduling, maintenance planning, and real-time fleet monitoring.This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚇 OverviewCurrently, two official plugins are available:

## 🚀 Quick Start

### Option 1: Complete Setup (First Time)

````bashKRONOS optimizes train fleet operations by:- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh

# Clone and setup everything from scratch

./setup-dev.sh- **Smart Scheduling**: AI-powered optimization for daily train assignments- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh



# Start the application- **Predictive Maintenance**: Health score monitoring and automatic maintenance scheduling

./start.sh

```- **Scenario Planning**: Handling normal operations, heavy monsoon, and festival surge scenarios## Expanding the ESLint configuration



### Option 2: Quick Launch (If Already Set Up)- **Real-time Monitoring**: Interactive dashboard showing fleet status and health metrics

```bash

# Just start the servers with existing data- **AI Chat Assistant**: RakeAssist chatbot for operational queries and insightsIf you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

./quick-start.sh



# Or regenerate data and start## 📋 Features

./run_all.sh

```### Backend (Python)

- **Optimization Engine**: Uses OR-Tools for constraint-based scheduling

### Option 3: Manual Setup- **AI Strategist**: Machine learning model for operational decision making

```bash- **Simulation Framework**: 30-day Monte Carlo simulation capabilities

# Backend setup- **RESTful API**: Flask-based API for frontend integration

cd backend- **Data Management**: Automated CSV/JSON data pipeline

python3 -m venv venv

source venv/bin/activate### Frontend (React + Vite)

pip install -r requirements.txt- **Fleet Dashboard**: Real-time visualization of train status

- **Interactive Calendar**: Day-by-day operation planning

# Configure environment- **Health Monitoring**: Train health scores and maintenance alerts

cp .env.example .env- **Chat Interface**: AI-powered operational assistant

# Edit .env with your API keys- **Responsive Design**: Modern UI with Tailwind CSS



# Initialize system## 🚀 Quick Start

python train_weight_predictor.py

python initialize_month.py### Prerequisites

python new_solver.py- Python 3.8+ with pip

python convert_csv_to_json.py- Node.js 16+ with npm

cp data/simulation_log.json ../public/- Git



# Start backend### Installation

python api_server.py &

1. **Clone the repository**

# Frontend setup (in new terminal)   ```bash

npm install   git clone <repository-url>

npm run dev   cd KRONOS-KRONOS_app

```   ```



## 📋 System Overview2. **Backend Setup**

   ```bash

KRONOS is an intelligent fleet management system that optimizes train operations using:   cd backend

   python -m venv venv

- **Constraint Programming**: OR-Tools solver for optimal scheduling   source venv/bin/activate  # On Windows: venv\Scripts\activate

- **Machine Learning**: Predictive models for maintenance and efficiency   pip install -r requirements.txt

- **Real-time Dashboard**: Interactive React interface   ```

- **AI Assistant**: Gemini-powered chatbot for insights

3. **Frontend Setup**

### Key Features   ```bash

   npm install

- 🧠 **AI-Powered Optimization** - Smart scheduling with constraint solving   ```

- 📊 **Interactive Dashboard** - Real-time fleet status and analytics

- 🤖 **Intelligent Chatbot** - Natural language fleet insights4. **Environment Configuration**

- 📈 **Predictive Analytics** - ML-based maintenance predictions   Create `backend/.env` with:

- 🔄 **Dynamic Simulation** - 30-day operational forecasting   ```

- 📱 **Responsive Design** - Works on desktop and mobile   GEMINI_API_KEY=your_google_gemini_api_key_here

````

## 🏗️ Architecture

### Running the Application

````

KRONOS/**Option 1: Full Automated Setup**

├── backend/                    # Python backend services```bash

│   ├── data/                  # CSV data and JSON outputs./run_all.sh

│   ├── models/                # Trained ML modelsnpm run dev

│   ├── new_solver.py          # Main optimization engine```

│   ├── api_server.py          # Flask API server

│   └── requirements.txt       # Python dependencies**Option 2: Manual Step-by-Step**

├── src/                       # React frontend source```bash

├── public/                    # Static assets and data# 1. Start backend services

├── setup-dev.sh              # Complete development setupcd backend

├── start.sh                  # Production start scriptsource venv/bin/activate

├── quick-start.sh            # Quick server launchpython train_weight_predictor.py

└── run_all.sh               # Data generation + launchpython initialize_month.py

```python new_solver.py

python convert_csv_to_json.py

## ⚙️ Configurationcp data/simulation_log.json ../public/

python api_server.py &

### Environment Variables

# 2. Start frontend (in new terminal)

Create `backend/.env`:npm run dev

```bash```

# Required: Gemini AI API Key for chatbot

GEMINI_API_KEY=your_google_gemini_api_key_hereVisit `http://localhost:5173` to access the application.



# Optional: Development settings## 📁 Project Structure

DEBUG=true

````

KRONOS-KRONOS_app/

### System Requirements├── README.md # This file

├── run_all.sh # Automated setup script

- **Python 3.8+** with pip├── package.json # Frontend dependencies

- **Node.js 16+** with npm├── vite.config.js # Vite configuration

- **Git** for version control├── tailwind.config.js # Tailwind CSS config

- **Google Gemini API Key** (for chatbot features)├── eslint.config.js # ESLint configuration

├── index.html # Main HTML template

## 🔧 Development├── public/ # Static assets

│ └── simulation_log.json # Frontend data source

### Project Structure├── src/ # React source code

````│ ├── App.jsx             # Main application component

Backend Components:│   ├── CalendarPicker.jsx   # Date selection component

- new_solver.py      → Main optimization engine│   ├── ChatbotModal.jsx     # AI assistant interface

- api_server.py      → Flask REST API│   ├── simulationUtils.js   # Data processing utilities

- initialize_month.py → Fleet data initialization│   ├── main.jsx            # React entry point

- train_weight_predictor.py → ML model training│   ├── App.css             # Global styles

- convert_csv_to_json.py → Data format conversion│   └── index.css           # Base styles

└── backend/                 # Python backend

Frontend Components:    ├── README.md           # Backend-specific documentation

- App.jsx           → Main application component    ├── requirements.txt    # Python dependencies

- ChatbotModal.jsx  → AI assistant interface    ├── .env               # Environment variables

- CalendarPicker.jsx → Date selection widget    ├── api_server.py      # Flask API server

- simulationUtils.js → Data processing utilities    ├── new_solver.py      # Main optimization engine

```    ├── initialize_month.py # Fleet initialization

    ├── train_weight_predictor.py # AI model training

### Available Scripts    ├── convert_csv_to_json.py # Data conversion

    ├── venv/              # Python virtual environment

```bash    ├── data/              # Data files

# Development    │   ├── fleet_data.csv

npm run dev          # Start development server    │   ├── fleet_status.csv

npm run build        # Build for production    │   ├── historical_data_retrain.csv

npm run preview      # Preview production build    │   ├── monthly_simulation_log.csv

    │   └── simulation_log.json

# Backend    └── models/            # Trained ML models

cd backend        ├── strategy_model.joblib

source venv/bin/activate        └── weight_predictor_model.joblib

python api_server.py          # Start API server```

python new_solver.py          # Run optimization

python train_weight_predictor.py  # Train ML models## 🔧 Configuration

````

### Scenario Settings

### API EndpointsThe system supports three operational scenarios:

- **NORMAL**: 6 trains in service, 2 maintenance slots

```````- **HEAVY_MONSOON**: 6 trains in service, 2 maintenance slots, weather penalties

GET  /api/health        → System health check- **FESTIVAL_SURGE**: 6 trains in service, 1 maintenance slot

POST /api/chat          → Chatbot interactions

GET  /api/simulation    → Simulation data### Fleet Parameters

POST /api/optimize      → Trigger optimization- **Fleet Size**: 25 trains (Rake-01 to Rake-25)

```- **Daily Operation**: 200km per train, 16 hours per branded train

- **Health Monitoring**: Automatic health score calculation

## 📊 Data Flow- **Maintenance Scheduling**: Predictive maintenance based on health scores



1. **Initialization** - `initialize_month.py` creates base fleet data## 🤖 AI Features

2. **Training** - `train_weight_predictor.py` builds ML models

3. **Optimization** - `new_solver.py` generates optimal schedules### RakeAssist Chatbot

4. **Conversion** - `convert_csv_to_json.py` formats for frontendAsk questions like:

5. **Display** - React app visualizes results and enables interaction- "Why was Rake-12 in maintenance on day 5?"

- "What happened to Rake-08 on day 10?"

## 🛠️ Troubleshooting- "Show me the health status for day 15"



### Common Issues### Optimization Engine

- Constraint-based scheduling using Google OR-Tools

**Backend won't start:**- Multi-objective optimization considering cost, health, and SLA compliance

```bash- Real-time decision making with manual override support

# Check Python environment

cd backend && source venv/bin/activate## 📊 API Endpoints

python --version  # Should be 3.8+

### Chat API

# Reinstall dependencies- **POST** `/chat` - Send queries to RakeAssist

pip install --upgrade pip  ```json

pip install -r requirements.txt  {

```    "message": "Why was Rake-12 in maintenance on day 5?"

  }

**Frontend build errors:**  ```

```bash

# Clear and reinstall## 🛠️ Development

rm -rf node_modules package-lock.json

npm install### Adding New Scenarios

```1. Update `SCENARIO_MODIFIERS` in `new_solver.py`

2. Modify `MONTHLY_SCENARIOS` calendar

**Missing data files:**3. Re-run simulation with `./run_all.sh`

```bash

# Regenerate all data### Customizing Fleet Size

cd backend && source venv/bin/activate1. Update train list in `initialize_month.py`

python initialize_month.py2. Adjust optimization constraints in `new_solver.py`

python train_weight_predictor.py3. Regenerate initial data

python new_solver.py

python convert_csv_to_json.py### Frontend Development

``````bash

npm run dev    # Development server

**Chatbot not working:**npm run build  # Production build

- Verify `GEMINI_API_KEY` in `backend/.env`npm run lint   # Code linting

- Check API key permissions and quotas```



### Performance Optimization### Backend Development

```bash

- **Large datasets**: Adjust batch sizes in solver configurationsource backend/venv/bin/activate

- **Memory usage**: Monitor Python process memory during optimizationpython backend/api_server.py  # Start API server

- **Response times**: Consider caching for frequently accessed datapython backend/new_solver.py  # Run optimization

```````

## 🔐 Security

## 📈 Performance

- API keys stored in environment variables

- No sensitive data in source control- **Optimization Speed**: ~1-2 seconds per day simulation

- Input validation on all API endpoints- **API Response Time**: <500ms for chat queries

- CORS configuration for development- **Frontend Load Time**: <2 seconds initial load

- **Memory Usage**: ~200MB backend, ~50MB frontend

## 📄 License

## 🚨 Troubleshooting

MIT License - see [LICENSE](LICENSE) file for details.

### Common Issues

## 🤝 Contributing

1. **"No simulation data found"**

1. Fork the repository - Run `./run_all.sh` to generate data

1. Create a feature branch (`git checkout -b feature/amazing-feature`) - Check `public/simulation_log.json` exists

1. Commit changes (`git commit -m 'Add amazing feature'`)

1. Push to branch (`git push origin feature/amazing-feature`)2. **Chat assistant not responding**

1. Open a Pull Request - Verify `GEMINI_API_KEY` in `backend/.env`

   - Check API server is running on port 5001

## 🆘 Support

3. **Optimization errors**

For issues and questions: - Ensure Python environment is activated

- Install missing packages: `pip install -r backend/requirements.txt`

1. Check the [troubleshooting section](#troubleshooting)

2. Review [backend documentation](backend/README.md)4. **Frontend build issues**

3. Open an issue with system details and error messages - Clear node_modules: `rm -rf node_modules && npm install`

   - Check Node.js version: `node --version`

---

## 📝 License

**KRONOS** - Intelligent Fleet Management for the Modern Era
This project is proprietary software. All rights reserved.

## 👥 Support

For technical support or questions, please contact the development team.

---

**KRONOS** - Optimizing Metro Operations with AI-Powered Intelligence
