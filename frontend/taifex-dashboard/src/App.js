import React, { useEffect, useState } from 'react';
import './App.css';
import DataChart from './DataChart';

function App() {
  const [data, setData] = useState(null);
  const [range, setRange] = useState('30'); // 默認顯示過去30天的數據

  useEffect(() => {
    fetch(`http://localhost:5000/api/data?start_date=${getStartDate(range)}`)
      .then(response => response.json())
      .then(data => setData(data.data))
      .catch(error => console.error('Error fetching data:', error));
  }, [range]);

  // 計算起始日期
  function getStartDate(days) {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>資料圖表展示</h1>
        <div>
          <button onClick={() => setRange('7')}>過去7天</button>
          <button onClick={() => setRange('30')}>過去30天</button>
          <button onClick={() => setRange('90')}>過去90天</button>
        </div>
        {data ? <DataChart data={data} /> : <p>加載中...</p>}
      </header>
    </div>
  );
}

export default App;
