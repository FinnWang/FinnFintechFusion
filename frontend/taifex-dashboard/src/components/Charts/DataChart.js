import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function DataChart({ filteredData }) {
  // 檢查 filteredData 是否存在
  if (!filteredData || filteredData.length === 0) {
    return <div>加載中...</div>; // 或者返回一個空的圖表
  }

  // 構建唯一的日期標籤
  const uniqueDates = [...new Set(filteredData.map(item => item.date))];

  // 構建數據集
  const chartData = {
    labels: uniqueDates,
    datasets: [
      {
        type: 'line',
        label: '多方口數',
        data: filteredData.map(item => item.long_position),
        borderColor: 'rgba(75,192,192,1)',
        yAxisID: 'y-axis-counts',
        fill: false,
      },
      {
        type: 'line',
        label: '空方口數',
        data: filteredData.map(item => item.short_position),
        borderColor: 'rgba(192,75,75,1)',
        yAxisID: 'y-axis-counts',
        fill: false,
      },
      {
        type: 'bar',
        label: '多方契約金額',
        data: filteredData.map(item => item.long_amount),
        backgroundColor: 'rgba(75,192,192,0.4)',
        yAxisID: 'y-axis-amount',
      },
      {
        type: 'bar',
        label: '空方契約金額',
        data: filteredData.map(item => item.short_amount),
        backgroundColor: 'rgba(192,75,75,0.4)',
        yAxisID: 'y-axis-amount',
      }
    ],
  };

  // 設置圖表選項
  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'day',
          displayFormats: {
            day: 'yyyy/MM/dd'
          }
        },
        title: {
          display: true,
          text: '日期'
        }
      },
      'y-axis-counts': {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: '口數'
        }
      },
      'y-axis-amount': {
        type: 'linear',
        position: 'right',
        title: {
          display: true,
          text: '金額'
        }
      }
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '多空口數與契約金額趨勢圖',
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default DataChart;
