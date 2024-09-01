import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function DataChart({ data }) {
  // 構建數據標籤（通常是日期）
  const labels = data.map(item => item.date);

  // 構建數據集（多方口數和空方口數）
  const chartData = {
    labels: labels,
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

  // 設置圖表選項
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '多空口數趨勢圖',
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default DataChart;
