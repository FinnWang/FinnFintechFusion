import { useState, useMemo } from 'react';
import { parseISO, isWithinInterval, subDays, startOfWeek, addDays, isWednesday } from 'date-fns';

function useDateFilter(data, initialRange = '7d') {
  const [dateRange, setDateRange] = useState(initialRange);

  // Helper function to check if a date is on the weekend
  const isWeekend = (date) => {
    const day = date.getDay();
    return day === 0 || day === 6; // 0 = Sunday, 6 = Saturday
  };

  const filteredData = useMemo(() => {
    const now = new Date();
    let filtered = [];

    if (dateRange === '7d') {
      filtered = data.filter(item => {
        const itemDate = parseISO(item.date);
        return isWithinInterval(itemDate, {
          start: subDays(now, 7),
          end: now
        }) && !isWeekend(itemDate);
      });
    } else if (dateRange === '15d') {
      filtered = data.filter(item => {
        const itemDate = parseISO(item.date);
        return isWithinInterval(itemDate, {
          start: subDays(now, 15),
          end: now
        }) && !isWeekend(itemDate);
      });
    } else if (dateRange === '30d') {
      filtered = data.filter(item => {
        const itemDate = parseISO(item.date);
        return isWithinInterval(itemDate, {
          start: subDays(now, 30),
          end: now
        }) && !isWeekend(itemDate);
      });
    } else if (dateRange === 'weekCycle') {
      // 特殊週期 (週三到下週二)
      let lastWednesday = startOfWeek(now, { weekStartsOn: 3 }); // 本週的週三
      if (!isWednesday(now)) {
        lastWednesday = subDays(lastWednesday, 7); // 如果今天不是週三，找上一個週三
      }
      const nextTuesday = addDays(lastWednesday, 6); // 下週二
      filtered = data.filter(item => {
        const itemDate = parseISO(item.date);
        return isWithinInterval(itemDate, {
          start: lastWednesday,
          end: nextTuesday
        });
      });
    }

    return filtered;
  }, [data, dateRange]); // 使用 useMemo，只在 data 或 dateRange 改變時重新計算

  return [filteredData, dateRange, setDateRange];
}

export default useDateFilter;
