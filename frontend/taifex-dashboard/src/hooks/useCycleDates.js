import { useMemo } from 'react';

export function useCycleDates() {
  return useMemo(() => {
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 (星期日) 到 6 (星期六)
    
    let startDate;
    let endDate = today;

    if (dayOfWeek === 0) { // 今天是星期日
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 4); // 上周三
    } else if (dayOfWeek === 1) { // 今天是星期一
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 5); // 上周三
    } else if (dayOfWeek === 2) { // 今天是星期二
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 6); // 上周三
    } else { // 今天是星期三到星期六
      startDate = new Date(today);
      startDate.setDate(today.getDate() - (dayOfWeek - 3)); // 这周三
    }

    // 确保返回的日期是有效的字符串格式
    return [
      startDate.toISOString().split('T')[0],
      endDate.toISOString().split('T')[0]
    ];
  }, []);
}
