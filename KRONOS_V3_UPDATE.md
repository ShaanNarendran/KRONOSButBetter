# KRONOSv3 Integration Update

## What Changed

Your frontend has been successfully updated to work with the new KRONOSv3 backend API instead of reading from static JSON files.

### Key Changes Made:

1. **Updated `src/App.jsx`**:

   - Added ExplainabilityModal component for AI explanations
   - Updated state management to handle AI explanations
   - Added proper error handling and loading states

2. **Completely rewrote `src/simulationUtils.js`**:

   - Now connects to Flask API at `http://localhost:5000` instead of reading JSON files
   - Added functions for:
     - `loadSimulationData()` - Calls `/run_full_simulation` API
     - `rerunSimulation()` - Calls `/rerun_from_day` API
     - `fetchExplanations()` - Calls `/get_explanations` API
   - Data transformation functions updated for new data structure

3. **Created new `src/ExplainabilityModal.jsx`**:
   - Beautiful modal showing SHAP explanations from AI decisions
   - Visual representation of feature impacts
   - Readable explanations for each AI strategy decision

### Backend API Endpoints (KRONOSv3)

- **POST** `/run_full_simulation` - Runs complete 30-day simulation
- **POST** `/rerun_from_day` - Reruns simulation from specific day with manual overrides
- **GET** `/get_explanations` - Fetches AI explainability data

### How to Run

1. **Setup the KRONOSv3 backend**:

   ```bash
   ./setup_backend_v3.sh
   ```

2. **Start your frontend** (in another terminal):
   ```bash
   npm run dev
   ```

### Data Flow

```
Frontend → Flask API (localhost:5000) → AI Models → Simulation Results → Frontend Display
```

### Fallback Behavior

If the API is unavailable, the app will fallback to reading from `public/simulation_log.json` to ensure it continues working.

### New Features Added

1. **AI Explainability**: View SHAP explanations for AI strategic decisions
2. **Real-time Simulation**: Backend generates fresh simulations instead of using static data
3. **Manual Overrides**: Ability to rerun simulations with custom parameters
4. **Enhanced Error Handling**: Better user feedback when API calls fail

Your existing UI components, styling, and user experience remain exactly the same - only the data source has changed from static JSON to dynamic API calls.
