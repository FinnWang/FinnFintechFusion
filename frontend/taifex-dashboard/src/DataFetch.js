import React, { useEffect, useState } from 'react';

function DataFetch() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/data')  // 使用您的 Flask API 地址
      .then(response => response.json())
      .then(data => setData(data.data))  // 注意這裡直接設置為返回的 data 字段
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>資料展示</h1>
      {data ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              <p>日期: {item.date}</p>
              <p>資料類型: {item.data_type}</p>
              <p>身分別: {item.identity}</p>
              <p>多方口數: {item.long_position}</p>
              <p>空方口數: {item.short_position}</p>
              <p>多空淨額口數: {item.net_position}</p>
              <hr />
            </li>
          ))}
        </ul>
      ) : (
        <p>加載中...</p>
      )}
    </div>
  );
}

export default DataFetch;
