import React, { useEffect, useState } from 'react';

function DataFetch() {
  const [data, setData] = useState(null);
  const [filteredData, setFilteredData] = useState(null);
  const [filterType, setFilterType] = useState('交易口數與契約金額');

  useEffect(() => {
    fetch('http://localhost:5000/api/data')  // 使用您的 Flask API 地址
      .then(response => response.json())
      .then(data => {
        setData(data.data);
        filterData(data.data, filterType); // 初始過濾
      })
      .catch(error => console.error('Error fetching data:', error));
      // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // 確保這個空依賴陣列正確地存在

  const filterData = (data, type) => {
    const filtered = data.filter(item => item.data_type === type);
    setFilteredData(filtered);
  };

  const handleFilterChange = (event) => {
    const selectedType = event.target.value;
    setFilterType(selectedType);
    if (data) {
      filterData(data, selectedType);
    }
  };

  return (
    <div>
      <h1>資料展示</h1>
      <label htmlFor="data-type-filter">選擇資料類型: </label>
      <select id="data-type-filter" value={filterType} onChange={handleFilterChange}>
        <option value="交易口數與契約金額">交易口數與契約金額</option>
        <option value="未平倉口數與契約金額">未平倉口數與契約金額</option>
      </select>
      {filteredData ? (
        <ul>
          {filteredData.map((item, index) => (
            <li key={index}>
              <p>日期: {item.date}</p>
              <p>資料類型: {item.data_type}</p>
              <p>身分別: {item.identity}</p>
              <p>多方口數: {item.long_position}</p>
              <p>多方契約金額: {item.long_amount}</p>
              <p>空方口數: {item.short_position}</p>
              <p>空方契約金額: {item.short_amount}</p>
              <p>多空淨額口數: {item.net_position}</p>
              <p>多空淨額金額: {item.net_amount}</p>
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
