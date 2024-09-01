import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,     // 必須註冊這個類別比例
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// 確保註冊了所有必要的元素
ChartJS.register(
  CategoryScale,     // 這是 x 軸的類別比例
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


function DataChart({ data }) {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: '多方口數',
        data: data.map(item => item.long_position),
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
      {
        label: '空方口數',
        data: data.map(item => item.short_position),
        borderColor: 'rgba(192,75,75,1)',
        fill: false,
      }
    ],
  };

  return <Line data={chartData} />;
}

export default DataChart;
