import { useState } from 'react';

// Constants
const API_BASE_URL = 'http://localhost:5001';

// Main simulation data loading function
export const loadSimulationData = async () => {
  // Try to get existing simulation data first, fallback to local JSON if it fails
  try {
    console.log('Attempting to load existing simulation data from API...');
    const response = await fetch(`${API_BASE_URL}/get_simulation_data`);
    
    if (response.ok) {
      const result = await response.json();
      if (result.status === 'success' && result.data) {
        console.log('Successfully loaded simulation data from API:', result.data.length, 'days');
        return result.data;
      }
    }
    
    console.log('No existing simulation data found, running new simulation...');
    const simResponse = await fetch(`${API_BASE_URL}/run_full_simulation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!simResponse.ok) {
      throw new Error(`API failed with status: ${simResponse.status}`);
    }

    const simResult = await simResponse.json();
    if (simResult.status === 'error') {
      throw new Error(simResult.message);
    }
    
    console.log('Successfully generated simulation data from API:', simResult.data?.length || 0, 'days');
    return simResult.data || [];
  } catch (error) {
    console.error('Failed to load simulation from API:', error);
    console.log('Falling back to local JSON file...');
    
    try {
      const response = await fetch('/simulation_log.json');
      if (!response.ok) {
        throw new Error('Failed to load simulation data');
      }
      const data = await response.json();
      console.log('Successfully loaded simulation data from JSON:', data.length, 'days');
      return data;
    } catch (fallbackError) {
      console.error('Error loading fallback simulation data:', fallbackError);
      return [];
    }
  }
  
  // TODO: Re-enable API calls once backend CORS is fixed
  /*
  try {
    const response = await fetch(`${API_BASE_URL}/run_full_simulation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error('Simulation failed');
    }

    const result = await response.json();
    if (result.status === 'error') {
      throw new Error(result.message);
    }
    
    return result.data || [];
  } catch (error) {
    console.error('Failed to load simulation from API:', error);
    // Fallback to local JSON file
    try {
      const response = await fetch('/simulation_log.json');
      if (!response.ok) {
        throw new Error('Failed to load fallback simulation data');
      }
      return await response.json();
    } catch (fallbackError) {
      console.error('Error loading fallback simulation data:', fallbackError);
      return [];
    }
  }
  */
};

// Rerun simulation from a specific day
export const rerunSimulation = async (startDay, overrides = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/rerun_from_day`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        start_day: startDay,
        manual_overrides: overrides
      })
    });

    if (!response.ok) {
      throw new Error('Rerun failed');
    }

    const result = await response.json();
    if (result.status === 'error') {
      throw new Error(result.message);
    }

    return result.data;
  } catch (error) {
    console.error('Failed to rerun simulation:', error);
    return null;
  }
};

// Fetch XAI explanations from the backend
export const fetchExplanations = async () => {
  try {
    console.log('Fetching AI explanations from backend...');
    const response = await fetch(`${API_BASE_URL}/get_explanations`);
    if (!response.ok) {
      throw new Error(`Failed to fetch explanations: ${response.status}`);
    }
    const result = await response.json();
    if (result.status === 'error') {
      throw new Error(result.message);
    }
    console.log('Successfully fetched explanations:', result.data?.length || 0, 'days');
    return result.data || [];
  } catch (error) {
    console.error('Error fetching explanations:', error);
    console.log('Falling back to empty explanations');
    return [];
  }
};

// Transform raw fleet data for UI display
export const transformFleetData = (simulationData, selectedDay) => {
  if (!simulationData || simulationData.length === 0) {
    console.log('No simulation data available');
    return [];
  }

  const dayData = simulationData.find(d => d.day === selectedDay);
  if (!dayData) {
    console.log(`No data found for day ${selectedDay}`);
    return [];
  }

  // Handle both old and new data formats
  const fleetData = dayData.fleet_status_today || dayData.fleet_status_after;
  if (!fleetData || !Array.isArray(fleetData)) {
    console.log('No fleet data available for day', selectedDay);
    return [];
  }

  console.log(`Transforming ${fleetData.length} trains for day ${selectedDay}`);

  return fleetData.map(train => {
    // Calculate a simple health score if not provided
    const healthScore = train.health_score || calculateSimpleHealthScore(train);
    
    // Determine status from plan
    let status = 'Standby';
    if (dayData.plan?.SERVICE?.includes(train.train_id)) {
      status = 'Service';
    } else if (dayData.plan?.MAINTENANCE?.includes(train.train_id)) {
      status = 'Maintenance';
    }

    return {
      id: train.train_id,
      status: status,
      healthScore: Math.round(healthScore),
      details: {
        fitnessCertificates: {
          status: train.is_cert_expired ? 'Expired' : 'Valid',
          expires: train.cert_telecom_expiry || 'Unknown'
        },
        jobCardStatus: {
          status: train.job_card_status || 'CLOSED',
          openJobs: train.job_card_status === 'OPEN' ? 1 : 0,
          details: train.job_card_priority || 'NONE'
        },
        brandingPriority: {
          level: train.branding_sla_active ? 'High' : 'Normal',
          contract: train.branding_sla_active ? 'Active' : 'None',
          exposureNeeded: train.target_hours ? `${train.target_hours}h needed` : 'N/A'
        },
        mileageBalancing: {
          status: (train.current_km || 0) > 55000 ? 'High' : 'Balanced',
          deviation: Math.abs(50000 - (train.current_km || 0)),
          unit: 'km'
        },
        cleaningDetailing: {
          status: 'Clean',
          lastCleaned: train.last_cleaned_date || 'Unknown'
        },
        stablingGeometry: {
          bay: `Bay ${(train.stabling_shunt_moves || 0) + 1}`,
          turnoutTime: `${(train.stabling_shunt_moves || 0) * 5} min`
        }
      }
    };
  });
};

// Simple health score calculation for fallback
function calculateSimpleHealthScore(train) {
  let score = 100;
  
  // Reduce score based on mileage
  if (train.current_km) {
    score -= Math.floor(train.current_km / 1000) * 2;
  }
  
  // Reduce score if certificate expired
  if (train.is_cert_expired) {
    score -= 30;
  }
  
  // Reduce score for open job cards
  if (train.job_card_status === 'OPEN') {
    score -= 20;
  }
  
  return Math.max(0, Math.min(100, score));
}

// Get summary statistics for the fleet
export const getFleetSummary = (simulationData, selectedDay) => {
  const dayData = simulationData.find(d => d.day === selectedDay);
  if (!dayData) return {
    total: 0,
    scenario: 'Normal',
    inService: 0,
    inMaintenance: 0,
    onStandby: 0
  };

  // Handle both old and new data formats
  const fleetData = dayData.fleet_status_after || dayData.fleet_status_today;
  const total = fleetData ? fleetData.length : 0;
  const inService = dayData.plan && dayData.plan.SERVICE ? dayData.plan.SERVICE.length : 0;
  const inMaintenance = dayData.plan && dayData.plan.MAINTENANCE ? dayData.plan.MAINTENANCE.length : 0;
  
  return {
    total,
    scenario: dayData.scenario ? 
      dayData.scenario.replace('_', ' ').replace(/\w\S*/g, 
        txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
      ) : 'Normal',
    inService,
    inMaintenance,
    onStandby: total - inService - inMaintenance
  };
};

// Custom hook for simulation data management
export const useSimulation = () => {
  const [simulationData, setSimulationData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await loadSimulationData();
      setSimulationData(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const rerunFromDay = async (day, overrides) => {
    setLoading(true);
    try {
      const data = await rerunSimulation(day, overrides);
      if (data) {
        setSimulationData(data);
        setError(null);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    simulationData,
    loading,
    error,
    loadData,
    rerunFromDay
  };
};