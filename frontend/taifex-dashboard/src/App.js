import React, { useEffect, useState } from 'react';
import './App.css';
import DataChart from './DataChart';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/data')
      .then(response => response.json())
      .then(data => setData(data.data))  // 確保設置數據後再渲染圖表
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>資料圖表展示</h1>
        {data ? <DataChart key={Math.random()} data={data} /> : <p>加載中...</p>}
      </header>
    </div>
  );
}

export default App;
