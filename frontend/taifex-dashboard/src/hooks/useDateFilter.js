import { useState, useMemo } from 'react';
import { parseISO, isWithinInterval, subDays, startOfWeek, format } from 'date-fns';

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
      // 特殊週期：從上週三開始，最多到本週五
      let startOfWeekWednesday = startOfWeek(now, { weekStartsOn: 3 }); // 本週的週三
      if (now < startOfWeekWednesday) {
        // 如果今天在本週三之前，那麼找到上週三
        startOfWeekWednesday = subDays(startOfWeekWednesday, 7);
      }

      const endDate = now; // 直接設置結束日期為今天

      filtered = data.filter(item => {
        const itemDate = parseISO(item.date);
        return isWithinInterval(itemDate, {
          start: startOfWeekWednesday,
          end: endDate,
        });
      });
    }

    // 格式化日期，將日期後面加上星期幾
    return filtered.map(item => ({
      ...item,
      date: format(parseISO(item.date), 'yyyy-MM-dd (EEE)'), // 格式化為 'YYYY-MM-DD (星期X)'
    }));
  }, [data, dateRange]); // 使用 useMemo，只在 data 或 dateRange 改變時重新計算

  return [filteredData, dateRange, setDateRange];
}

export default useDateFilter;
