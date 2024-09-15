import React, { useEffect, useState } from 'react';
import DataChart from '../Charts/DataChart'; // 正確的相對路徑

function DataFetch() {
  const [data, setData] = useState(null);
  const [filteredData, setFilteredData] = useState([]);
  const [filterType, setFilterType] = useState('交易口數與契約金額'); // 默認資料類型
  const [filterIdentity, setFilterIdentity] = useState('自營商'); // 默認身份

  useEffect(() => {
    fetch('http://localhost:5000/api/data')  // 使用您的 Flask API 地址
      .then(response => response.json())
      .then(data => {
        setData(data.data);
        filterData(data.data, filterType, filterIdentity); // 初始過濾
      })
      .catch(error => console.error('Error fetching data:', error));
      // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 過濾數據的方法
  const filterData = (data, type, identity) => {
    const filtered = data.filter(item => item.data_type === type && item.identity === identity);
    setFilteredData(filtered);
  };

  // 處理資料類型過濾條件改變
  const handleFilterTypeChange = (event) => {
    const selectedType = event.target.value;
    setFilterType(selectedType);
    if (data) {
      filterData(data, selectedType, filterIdentity);
    }
  };

  // 處理身份過濾條件改變
  const handleFilterIdentityChange = (event) => {
    const selectedIdentity = event.target.value;
    setFilterIdentity(selectedIdentity);
    if (data) {
      filterData(data, filterType, selectedIdentity);
    }
  };

  return (
    <div>
      <h1>資料展示</h1>
      
      {/* 資料類型選擇 */}
      <label htmlFor="data-type-filter">選擇資料類型: </label>
      <select id="data-type-filter" value={filterType} onChange={handleFilterTypeChange}>
        <option value="交易口數與契約金額">交易口數與契約金額</option>
        <option value="未平倉口數與契約金額">未平倉口數與契約金額</option>
      </select>

      {/* 身份選擇 */}
      <label htmlFor="identity-filter">選擇身份: </label>
      <select id="identity-filter" value={filterIdentity} onChange={handleFilterIdentityChange}>
        <option value="自營商">自營商</option>
        <option value="投信">投信</option>
        <option value="外資">外資</option>
        <option value="合計">合計</option>
      </select>

      {/* 傳遞 filteredData 給 DataChart */}
      <DataChart filteredData={filteredData} />

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
