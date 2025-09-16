import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const CalendarPicker = ({ onDateSelect, selectedDay }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  
  // Base date for simulation (September 16, 2025)
  const baseDate = new Date(2025, 8, 16); // Month is 0-indexed
  
  // Generate calendar days for the current month view
  const generateCalendarDays = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startOfWeek = new Date(firstDay);
    startOfWeek.setDate(firstDay.getDate() - firstDay.getDay());
    
    const days = [];
    const current = new Date(startOfWeek);
    
    // Generate 6 weeks of days
    for (let week = 0; week < 6; week++) {
      for (let day = 0; day < 7; day++) {
        const date = new Date(current);
        const isCurrentMonth = date.getMonth() === month;
        
        // Calculate simulation day (1-30) based on days from base date
        const dayDiff = Math.floor((date - baseDate) / (1000 * 60 * 60 * 24));
        const simulationDay = dayDiff >= 0 && dayDiff < 30 ? dayDiff + 1 : null;
        
        days.push({
          date: new Date(date),
          day: date.getDate(),
          isCurrentMonth,
          simulationDay,
          isToday: date.toDateString() === new Date().toDateString(),
          isSelected: simulationDay === selectedDay
        });
        
        current.setDate(current.getDate() + 1);
      }
    }
    
    return days;
  };

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const navigateMonth = (direction) => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setMonth(prev.getMonth() + direction);
      return newDate;
    });
  };

  const handleDayClick = (dayInfo) => {
    if (dayInfo.simulationDay && dayInfo.isCurrentMonth) {
      onDateSelect(dayInfo.simulationDay, dayInfo.date);
    }
  };

  const calendarDays = generateCalendarDays();

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-600 p-6 shadow-xl">
      {/* Calendar Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => navigateMonth(-1)}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <ChevronLeft size={20} className="text-gray-400" />
        </button>
        
        <h3 className="text-xl font-semibold text-white">
          {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h3>
        
        <button
          onClick={() => navigateMonth(1)}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <ChevronRight size={20} className="text-gray-400" />
        </button>
      </div>

      {/* Day Labels */}
      <div className="grid grid-cols-7 gap-1 mb-2">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="p-2 text-center text-sm font-medium text-gray-400">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays.map((dayInfo, index) => {
          const canSelect = dayInfo.simulationDay && dayInfo.isCurrentMonth;
          
          return (
            <button
              key={index}
              onClick={() => handleDayClick(dayInfo)}
              disabled={!canSelect}
              className={`
                p-3 text-sm rounded-lg transition-all duration-200 relative
                ${dayInfo.isCurrentMonth 
                  ? 'text-white' 
                  : 'text-gray-600'
                }
                ${canSelect 
                  ? 'hover:bg-teal-500/20 hover:border-teal-400/30 border border-transparent cursor-pointer' 
                  : 'cursor-not-allowed'
                }
                ${dayInfo.isSelected 
                  ? 'bg-teal-500/30 border-teal-400 text-teal-100' 
                  : ''
                }
                ${dayInfo.isToday 
                  ? 'ring-2 ring-yellow-400/50' 
                  : ''
                }
              `}
            >
              <div className="flex flex-col items-center">
                <span className={`${dayInfo.isSelected ? 'font-bold' : ''}`}>
                  {dayInfo.day}
                </span>
                {dayInfo.simulationDay && (
                  <span className="text-xs text-teal-300 mt-1">
                    Day {dayInfo.simulationDay}
                  </span>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-4 text-xs text-gray-400 space-y-1">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-teal-500/30 border border-teal-400 rounded"></div>
          <span>Selected simulation day</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 ring-2 ring-yellow-400/50 rounded"></div>
          <span>Today</span>
        </div>
        <div className="text-gray-500">
          Simulation runs from September 16, 2025 for 30 days
        </div>
      </div>
    </div>
  );
};

export default CalendarPicker;