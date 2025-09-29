import React from 'react';
import { X, Brain, TrendingUp, TrendingDown, Minus } from 'lucide-react';

const ExplainabilityModal = ({ isOpen, onClose, explanations, selectedDay }) => {
  if (!isOpen) return null;

  const dayExplanations = explanations.find(e => e.day === selectedDay);
  
  if (!dayExplanations) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
        <div 
          className="bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800 rounded-3xl border-2 border-orange-400/50 w-full max-w-4xl shadow-2xl p-8"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-transparent bg-gradient-to-r from-orange-400 to-green-500 bg-clip-text">
              AI Explainability - Day {selectedDay}
            </h2>
            <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
              <X size={24} />
            </button>
          </div>
          
          <div className="text-center text-gray-400">
            <p>No AI explanations available for Day {selectedDay}</p>
          </div>
        </div>
      </div>
    );
  }

  const getImpactIcon = (value) => {
    const absValue = Math.abs(value);
    if (absValue < 0.05) return <Minus size={16} className="text-gray-400" />;
    return value > 0 ? 
      <TrendingUp size={16} className="text-green-400" /> : 
      <TrendingDown size={16} className="text-red-400" />;
  };

  const getImpactColor = (value) => {
    const absValue = Math.abs(value);
    if (absValue < 0.05) return 'text-gray-400';
    if (absValue < 0.15) return value > 0 ? 'text-green-400' : 'text-red-400';
    return value > 0 ? 'text-green-500' : 'text-red-500';
  };

  const getImpactIntensity = (value) => {
    const absValue = Math.abs(value);
    if (absValue < 0.05) return 'No Impact';
    if (absValue < 0.15) return 'Moderate';
    return 'Strong';
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div 
        className="bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800 rounded-3xl border-2 border-orange-400/50 w-full max-w-6xl shadow-2xl p-8 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-orange-500/10 to-transparent rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-green-500/10 to-transparent rounded-full blur-3xl"></div>
        
        <div className="relative z-10">
          <div className="flex justify-between items-center mb-8">
            <div className="flex items-center gap-3">
              <Brain className="text-orange-400" size={32} />
              <div>
                <h2 className="text-3xl font-bold text-transparent bg-gradient-to-r from-orange-400 to-green-500 bg-clip-text">
                  AI Explainability
                </h2>
                <p className="text-gray-400">Day {selectedDay} Strategic Decisions</p>
              </div>
            </div>
            <button 
              onClick={onClose} 
              className="text-gray-400 hover:text-white transition-all duration-300 p-3 hover:bg-gray-700/50 rounded-xl group"
            >
              <X size={28} className="group-hover:scale-110 transition-transform duration-300" />
            </button>
          </div>

          <div className="grid gap-8">
            {dayExplanations.shap_explanations.map((explanation, index) => (
              <div key={index} className="bg-gradient-to-r from-gray-900/80 via-gray-800/80 to-gray-900/80 p-6 rounded-2xl border border-gray-600/50 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-3 h-3 bg-orange-400 rounded-full"></div>
                  <h3 className="text-xl font-bold text-orange-300">
                    {explanation.output_name.replace('historical_', '').replace('_', ' ').toUpperCase()}
                  </h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-3">Feature Impact Analysis</h4>
                    <div className="space-y-3">
                      {explanation.shap_values.map((value, featureIndex) => {
                        const featureName = explanation.feature_names && explanation.feature_names[featureIndex] 
                          ? explanation.feature_names[featureIndex] 
                          : `Feature ${featureIndex + 1}`;
                        const featureValue = explanation.feature_values && explanation.feature_values[featureIndex] 
                          ? explanation.feature_values[featureIndex] 
                          : 'N/A';
                        
                        return (
                          <div key={featureIndex} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                            <div className="flex items-center gap-3">
                              {getImpactIcon(value)}
                              <div>
                                <span className="text-white font-medium">{featureName}</span>
                                <div className="text-sm text-gray-400">Value: {featureValue}</div>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className={`font-bold ${getImpactColor(value)}`}>
                                {value > 0 ? '+' : ''}{value.toFixed(3)}
                              </div>
                              <div className="text-xs text-gray-400">
                                {getImpactIntensity(value)}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-3">Readable Explanations</h4>
                    <div className="space-y-2">
                      {explanation.readable && explanation.readable.map((readableText, readableIndex) => (
                        <div key={readableIndex} className="p-3 bg-gray-700/30 rounded-lg">
                          <p className="text-gray-300 text-sm">{readableText}</p>
                        </div>
                      ))}
                    </div>
                    

                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-8 p-6 bg-gradient-to-r from-blue-900/30 via-gray-800/50 to-blue-900/30 rounded-2xl border border-blue-400/30">
            <h3 className="text-lg font-bold text-blue-300 mb-3">Understanding SHAP Values</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
              <div className="flex items-start gap-2">
                <TrendingUp size={16} className="text-green-400 mt-0.5" />
                <div>
                  <span className="font-medium text-green-300">Positive Impact:</span>
                  <p>Features that increase the predicted value</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <TrendingDown size={16} className="text-red-400 mt-0.5" />
                <div>
                  <span className="font-medium text-red-300">Negative Impact:</span>
                  <p>Features that decrease the predicted value</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <Minus size={16} className="text-gray-400 mt-0.5" />
                <div>
                  <span className="font-medium text-gray-300">Neutral Impact:</span>
                  <p>Features with minimal effect on the decision</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExplainabilityModal;