# 🚀 KRONOS - AI-Powered Fleet Management System

[![GitHub](https://img.shields.io/github/license/ShaanNarendran/KRONOSButBetter)](https://github.com/ShaanNarendran/KRONOSButBetter)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

KRONOS is an advanced fleet management system powered by AI optimization and machine learning explainability. It provides real-time fleet scheduling, maintenance optimization, and transparent AI decision-making through SHAP explanations.

## ✨ Features

### 🧠 AI-Powered Optimization
- **OR-Tools Integration**: Advanced constraint programming for optimal fleet scheduling
- **Machine Learning**: Predictive models for maintenance and operational decisions  
- **SHAP Explanations**: Transparent AI reasoning with feature impact visualization

### 📊 Fleet Management
- **Real-time Dashboard**: Monitor vehicle status, schedules, and maintenance
- **Dynamic Scheduling**: Automated optimization based on constraints and priorities
- **Historical Analytics**: Track performance trends and decision outcomes

### 🔍 Explainable AI
- **Decision Transparency**: See exactly why the AI made specific choices
- **Feature Impact**: Understand which factors influenced each decision
- **Interactive Explanations**: Explore AI reasoning through intuitive visualizations

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control

### One-Command Setup & Run

```bash
# Clone the repository
git clone https://github.com/ShaanNarendran/KRONOSButBetter.git
cd KRONOSButBetter

# Setup backend (one-time)
./setup_backend_v3.sh

# Run the complete application
./run_kronos.sh
```

That's it! 🎉

- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:5001
- **AI Explanations**: Menu (≡) → Explainability

## 📁 Project Structure

```
KRONOSButBetter/
├── 🚀 Quick Start Scripts
│   ├── setup_backend_v3.sh     # One-time backend setup
│   ├── run_kronos.sh            # Complete app launcher  
│   └── cleanup_old_files.sh     # Project cleanup utility
│
├── 🧠 AI Backend (KRONOSv3)
│   ├── backend_v3/
│   │   ├── backend_run_rerun.py # Flask API server
│   │   ├── answer_final.py      # Core optimization logic
│   │   ├── brain_make.py        # ML model training
│   │   └── *.csv, *.json       # Training data & models
│
├── 🎨 React Frontend  
│   ├── src/
│   │   ├── App.jsx              # Main dashboard
│   │   ├── ExplainabilityModal.jsx # AI explanations UI
│   │   ├── simulationUtils.js   # API communication
│   │   └── *.jsx, *.css        # Components & styles
│
└── ⚙️ Configuration
    ├── package.json             # Frontend dependencies
    ├── vite.config.js           # Build configuration
    └── tailwind.config.js       # Styling framework
```

## 🔧 Development

### Manual Setup (Alternative)

```bash
# Backend setup
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors ortools numpy pandas scikit-learn shap

# Frontend setup  
npm install

# Run backend (terminal 1)
cd backend_v3
python backend_run_rerun.py

# Run frontend (terminal 2)  
npm run dev
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/run_full_simulation` | Execute 30-day fleet optimization |
| GET | `/get_simulation_data` | Retrieve current simulation results |
| POST | `/rerun_from_day` | Rerun simulation from specific day |
| GET | `/get_explanations` | Get SHAP explanations for AI decisions |

## 🧠 AI Explainability

KRONOS uses **SHAP (SHapley Additive exPlanations)** to make AI decisions transparent:

### How It Works
1. **TreeExplainer**: Analyzes decision tree-based models
2. **Feature Impact**: Quantifies how each input affects the decision  
3. **Visual Explanations**: Shows positive/negative feature contributions
4. **Decision Context**: Provides readable explanations for each choice

### What You Can Explore
- **Fleet Utilization Factors**: Vehicle availability, maintenance windows
- **Cost Optimization**: Operational costs vs. service quality trade-offs  
- **Constraint Satisfaction**: How scheduling constraints influence decisions
- **Risk Assessment**: Factors affecting maintenance and safety priorities

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight web framework for API
- **OR-Tools**: Google's optimization toolkit  
- **SHAP**: Machine learning explainability
- **scikit-learn**: ML models and preprocessing
- **Pandas/NumPy**: Data manipulation and analysis

### Frontend  
- **React 18**: Modern UI library with hooks
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first styling framework
- **Lucide React**: Beautiful, consistent icons

### AI/ML
- **Constraint Programming**: Complex scheduling optimization
- **Ensemble Methods**: Robust predictive modeling
- **Feature Engineering**: Domain-specific input processing  
- **Model Interpretability**: SHAP-based explanations

## 📊 Use Cases

### Fleet Management Companies
- Optimize vehicle routing and scheduling
- Predict maintenance needs and costs
- Balance service quality with operational efficiency

### Logistics Operations  
- Coordinate multi-vehicle deliveries
- Minimize fuel costs and travel time
- Ensure regulatory compliance and safety

### Research & Education
- Study AI explainability in real applications  
- Analyze constraint optimization problems
- Explore human-AI interaction patterns

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (`./run_kronos.sh`)
5. Commit with clear messages
6. Push and create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **KRONOSv3**: Backend optimization engine
- **Google OR-Tools**: Constraint programming framework  
- **SHAP Team**: Machine learning explainability library
- **React Community**: Frontend development ecosystem

---

**Built with ❤️ for transparent, explainable AI in fleet management**

[🌟 Star this repo](https://github.com/ShaanNarendran/KRONOSButBetter) | [🐛 Report Issues](https://github.com/ShaanNarendran/KRONOSButBetter/issues) | [💡 Request Features](https://github.com/ShaanNarendran/KRONOSButBetter/issues/new)