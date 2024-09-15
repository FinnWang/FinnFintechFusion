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

function DataChart({ filteredData, viewType }) {
  if (!filteredData || filteredData.length === 0) {
    return <div>加載中或沒有數據...</div>;
  }

  const uniqueDates = [...new Set(filteredData.map(item => item.date))];
  const datasets = [];

  // 為紅綠色弱者選擇的顏色組合
  const colors = {
    '自營商': {
      baseColor: '#377eb8', // 藍色
    },
    '投信': {
      baseColor: '#ff7f00', // 橘色
    },
    '外資': {
      baseColor: '#e41a1c', // 紅色
    },
    '合計': {
      baseColor: '#a65628', // 褐色
    }
  };

  const identities = [...new Set(filteredData.map(item => item.identity))];
  
  identities.forEach(identity => {
    const identityData = filteredData.filter(item => item.identity === identity);
    const color = colors[identity] || { baseColor: '#000000' }; // 預設黑色

    // 深色和淺色，用於多方和空方
    const deepColor = color.baseColor; // 用於多方
    const lightColor = hexToRgba(color.baseColor, 0.5); // 用於空方，淺色
    const deepColorBackground = hexToRgba(color.baseColor, 0.8);
    const lightColorBackground = hexToRgba(color.baseColor, 0.3);

    if (viewType === 'all' || viewType === 'long') {
      datasets.push({
        type: 'line',
        label: `${identity} 多方口數`,
        data: identityData.map(item => item.long_position),
        borderColor: deepColor,
        yAxisID: 'y-axis-counts',
        fill: false,
      });

      datasets.push({
        type: 'bar',
        label: `${identity} 多方契約金額`,
        data: identityData.map(item => item.long_amount),
        backgroundColor: deepColorBackground,
        yAxisID: 'y-axis-amount',
      });
    }

    if (viewType === 'all' || viewType === 'short') {
      datasets.push({
        type: 'line',
        label: `${identity} 空方口數`,
        data: identityData.map(item => item.short_position),
        borderColor: lightColor,
        yAxisID: 'y-axis-counts',
        fill: false,
      });

      datasets.push({
        type: 'bar',
        label: `${identity} 空方契約金額`,
        data: identityData.map(item => item.short_amount),
        backgroundColor: lightColorBackground,
        yAxisID: 'y-axis-amount',
      });
    }
  });

  const chartData = {
    labels: uniqueDates,
    datasets: datasets,
  };

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

// 輔助函數：將十六進制顏色轉換為 RGBA 顏色
function hexToRgba(hex, alpha) {
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;

  return `rgba(${r},${g},${b},${alpha})`;
}

export default DataChart;
