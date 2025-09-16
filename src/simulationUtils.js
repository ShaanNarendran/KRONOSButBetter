// Utility functions to transform simulation log data for the UI

export const transformFleetData = (simulationData, selectedDay) => {
  if (!simulationData || !selectedDay) return [];
  
  // Find the data for the selected day
  const dayData = simulationData.find(entry => entry.day === selectedDay);
  if (!dayData) return [];
  
  // Transform the fleet_status_today data to match the UI format
  return dayData.fleet_status_today.map(train => {
    // Calculate health score based on various factors
    const healthScore = calculateHealthScore(train);
    
    // Determine status based on plan assignment
    let status = 'Unknown';
    if (dayData.plan.SERVICE.includes(train.train_id)) {
      status = 'Service';
    } else if (dayData.plan.MAINTENANCE.includes(train.train_id)) {
      status = 'Maintenance';
    } else if (dayData.plan.STANDBY.includes(train.train_id)) {
      status = 'Standby';
    }
    
    return {
      id: train.train_id,
      healthScore: Math.round(healthScore),
      status: status,
      details: {
        fitnessCertificates: {
          status: train.is_cert_expired ? 'Expired' : 'Valid',
          expires: train.cert_telecom_expiry
        },
        jobCardStatus: {
          status: train.job_card_status,
          openJobs: train.job_card_status === 'OPEN' ? 1 : 0,
          details: train.job_card_priority !== 'NONE' ? train.job_card_priority : 'No open jobs'
        },
        brandingPriority: {
          level: train.branding_sla_active ? 'High' : 'Low',
          contract: train.branding_sla_active ? 'Active Contract' : 'None',
          exposureNeeded: train.branding_sla_active 
            ? `${train.target_hours - train.current_hours} hrs remaining`
            : 'N/A'
        },
        mileageBalancing: {
          deviation: train.current_km - (train.target_km * 0.5), // Assuming 50% of target as baseline
          unit: 'km',
          status: getMileageStatus(train.current_km, train.target_km)
        },
        cleaningDetailing: {
          lastCleaned: train.last_cleaned_date,
          status: getCleaningStatus(train.last_cleaned_date)
        },
        stablingGeometry: {
          bay: `Bay ${train.stabling_shunt_moves + 1}`, // Simple bay assignment
          turnoutTime: `${train.stabling_shunt_moves * 2 + 3} mins`
        },
        // Additional details from simulation data
        consecutiveServiceDays: train.consecutive_service_days,
        totalServiceDaysMonth: train.total_service_days_month,
        totalMaintenanceDaysMonth: train.total_maintenance_days_month,
        brakeModel: train.brake_model,
        kmSinceLastService: train.km_since_last_service,
        bogieLastServiceKm: train.bogie_last_service_km
      }
    };
  });
};

const calculateHealthScore = (train) => {
  let score = train.health_score || 100;
  
  // Adjust based on certificate expiry
  if (train.is_cert_expired) {
    score -= 20;
  }
  
  // Adjust based on job card status
  if (train.job_card_status === 'OPEN') {
    score -= 10;
  }
  
  // Adjust based on km since last service
  if (train.km_since_last_service > 2000) {
    score -= 5;
  }
  
  // Adjust based on cleaning
  const daysSinceClean = getDaysSinceLastClean(train.last_cleaned_date);
  if (daysSinceClean > 7) {
    score -= 5;
  }
  
  return Math.max(0, Math.min(100, score));
};

const getMileageStatus = (currentKm, targetKm) => {
  const utilizationRate = currentKm / targetKm;
  
  if (utilizationRate < 0.3) {
    return 'Under-utilized';
  } else if (utilizationRate > 0.7) {
    return 'Over-utilized';
  } else {
    return 'Balanced';
  }
};

const getCleaningStatus = (lastCleanedDate) => {
  const daysSince = getDaysSinceLastClean(lastCleanedDate);
  
  if (daysSince <= 3) {
    return 'Clean';
  } else if (daysSince <= 7) {
    return 'Good';
  } else {
    return 'Due for Cleaning';
  }
};

const getDaysSinceLastClean = (lastCleanedDate) => {
  const today = new Date();
  const cleanDate = new Date(lastCleanedDate);
  const diffTime = Math.abs(today - cleanDate);
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

export const getFleetSummary = (simulationData, selectedDay) => {
  if (!simulationData || !selectedDay) {
    return {
      total: 0,
      service: 0,
      maintenance: 0,
      standby: 0,
      scenario: 'Unknown'
    };
  }
  
  const dayData = simulationData.find(entry => entry.day === selectedDay);
  if (!dayData) {
    return {
      total: 0,
      service: 0,
      maintenance: 0,
      standby: 0,
      scenario: 'Unknown'
    };
  }
  
  return {
    total: dayData.fleet_status_today.length,
    service: dayData.plan.SERVICE.length,
    maintenance: dayData.plan.MAINTENANCE.length,
    standby: dayData.plan.STANDBY.length,
    scenario: dayData.scenario
  };
};

export const getHealthDistribution = (fleetData) => {
  if (!fleetData || fleetData.length === 0) {
    return {
      excellent: 0,
      good: 0,
      fair: 0,
      poor: 0
    };
  }
  
  const distribution = fleetData.reduce((acc, train) => {
    const score = train.healthScore;
    if (score >= 90) acc.excellent++;
    else if (score >= 75) acc.good++;
    else if (score >= 60) acc.fair++;
    else acc.poor++;
    return acc;
  }, { excellent: 0, good: 0, fair: 0, poor: 0 });
  
  return distribution;
};

// Load simulation data from JSON file
export const loadSimulationData = async () => {
  try {
    const response = await fetch('/simulation_log.json');
    if (!response.ok) {
      throw new Error('Failed to load simulation data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error loading simulation data:', error);
    return [];
  }
};