import React, { useEffect, useState } from 'react';
import DataChart from '../Charts/DataChart'; // 確保這是正確的導入路徑

function DataFetch() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [filterType, setFilterType] = useState('交易口數與契約金額'); 
  const [selectedIdentities, setSelectedIdentities] = useState(['自營商']); 
  const [viewType, setViewType] = useState('all'); // 新增一個狀態來控制查看多方或空方

  useEffect(() => {
    fetch('http://localhost:5000/api/data')  // 使用您的 Flask API 地址
      .then(response => response.json())
      .then(data => {
        setData(data.data);
        filterData(data.data, filterType, selectedIdentities); // 初始過濾
      })
      .catch(error => console.error('Error fetching data:', error));
      // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 過濾數據的方法
  const filterData = (data, type, identities) => {
    const filtered = data.filter(item => item.data_type === type && identities.includes(item.identity));
    setFilteredData(filtered);
  };

  // 處理資料類型過濾條件改變
  const handleFilterTypeChange = (event) => {
    const selectedType = event.target.value;
    setFilterType(selectedType);
    if (data) {
      filterData(data, selectedType, selectedIdentities);
    }
  };

  // 處理身份多選框的改變
  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    const updatedIdentities = checked
      ? [...selectedIdentities, value]
      : selectedIdentities.filter(identity => identity !== value);

    setSelectedIdentities(updatedIdentities);
    filterData(data, filterType, updatedIdentities);
  };

  // 處理查看類型
  const handleViewTypeChange = (event) => {
    setViewType(event.target.value);
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

      {/* 身份多選框 */}
      <div>
        <label>
          <input
            type="checkbox"
            value="自營商"
            checked={selectedIdentities.includes('自營商')}
            onChange={handleCheckboxChange}
          /> 自營商
        </label>
        <label>
          <input
            type="checkbox"
            value="投信"
            checked={selectedIdentities.includes('投信')}
            onChange={handleCheckboxChange}
          /> 投信
        </label>
        <label>
          <input
            type="checkbox"
            value="外資"
            checked={selectedIdentities.includes('外資')}
            onChange={handleCheckboxChange}
          /> 外資
        </label>
        <label>
          <input
            type="checkbox"
            value="合計"
            checked={selectedIdentities.includes('合計')}
            onChange={handleCheckboxChange}
          /> 合計
        </label>
      </div>

      {/* 增加篩選按鈕 */}
      <div>
        <label>
          <input
            type="radio"
            name="viewType"
            value="all"
            checked={viewType === 'all'}
            onChange={handleViewTypeChange}
          /> 全部
        </label>
        <label>
          <input
            type="radio"
            name="viewType"
            value="long"
            checked={viewType === 'long'}
            onChange={handleViewTypeChange}
          /> 只看多方
        </label>
        <label>
          <input
            type="radio"
            name="viewType"
            value="short"
            checked={viewType === 'short'}
            onChange={handleViewTypeChange}
          /> 只看空方
        </label>
      </div>

      {/* 傳遞 filteredData 和 viewType 給 DataChart */}
      <DataChart filteredData={filteredData} viewType={viewType} />
    </div>
  );
}

export default DataFetch;
