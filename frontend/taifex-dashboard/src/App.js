import React, { useEffect, useState, useMemo } from 'react';
import './App.css';
import DataChart from './components/DataChart';
import { useCycleDates } from './hooks/useCycleDates';
import { Oval } from 'react-loader-spinner';

function App() {
  const [data, setData] = useState(null);
  const [dataTypes, setDataTypes] = useState([]); // 選擇的 data_type
  const [identities, setIdentities] = useState([]); // 選擇的 identity
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤狀態
  const [dateRange, setDateRange] = useState('7'); // 默認為7天
  const cycleDates = useCycleDates(); // 使用自定義 Hook 計算日期範圍

  useEffect(() => {
    let startDate, endDate;

    if (dateRange === 'custom') {
      console.log('Using custom cycle dates:', cycleDates);
      if (cycleDates.length > 0) {
        startDate = new Date(cycleDates[0]);
        endDate = new Date(cycleDates[1]);
      } else {
        console.error('Cycle dates are empty or invalid.');
        return;
      }
    } else {
      endDate = new Date();
      startDate = new Date();
      startDate.setDate(endDate.getDate() - parseInt(dateRange, 10));
    }

    console.log('Start Date:', startDate, 'End Date:', endDate);

    setLoading(true);

    fetch(`http://localhost:5000/api/data?start_date=${startDate.toISOString().split('T')[0]}&end_date=${endDate.toISOString().split('T')[0]}`)
      .then(response => response.json())
      .then(data => {
        setData(data.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error);
        setLoading(false);
      });
  }, [dateRange, cycleDates]);

  useEffect(() => {
    // 设置默认选择
    setDataTypes(['未平倉口數與契約金額']);
    setIdentities(['自營商']);
  }, []);

  const handleDataTypeChange = (event) => {
    const { value, checked } = event.target;
    setDataTypes(checked ? [...dataTypes, value] : dataTypes.filter(dt => dt !== value));
  };

  const handleIdentityChange = (event) => {
    const { value, checked } = event.target;
    setIdentities(checked ? [...identities, value] : identities.filter(id => id !== value));
  };

  const handleDateRangeChange = (range) => {
    setDateRange(range);
  };

  const filteredData = useMemo(() => {
    return data ? data.filter(item => 
      (dataTypes.length === 0 || dataTypes.includes(item.data_type)) &&
      (identities.length === 0 || identities.includes(item.identity))
    ) : [];
  }, [data, dataTypes, identities]);

  const reversedData = useMemo(() => [...filteredData].reverse(), [filteredData]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>資料圖表展示</h1>

        <div>
          <h3>選擇日期範圍</h3>
          <button onClick={() => handleDateRangeChange('7')}>過去7天</button>
          <button onClick={() => handleDateRangeChange('15')}>過去15天</button>
          <button onClick={() => handleDateRangeChange('30')}>過去30天</button>
          <button onClick={() => handleDateRangeChange('custom')}>本周周期</button>
        </div>
        
        <div>
          <h3>選擇資料類型</h3>
          <label>
            <input type="checkbox" value="未平倉口數與契約金額" onChange={handleDataTypeChange} />
            未平倉口數與契約金額
          </label>
          <label>
            <input type="checkbox" value="交易口數與契約金額" onChange={handleDataTypeChange} />
            交易口數與契約金額
          </label>
        </div>

        <div>
          <h3>選擇身份別</h3>
          <label>
            <input type="checkbox" value="自營商" onChange={handleIdentityChange} />
            自營商
          </label>
          <label>
            <input type="checkbox" value="投信" onChange={handleIdentityChange} />
            投信
          </label>
          <label>
            <input type="checkbox" value="外資" onChange={handleIdentityChange} />
            外資
          </label>
          <label>
            <input type="checkbox" value="合計" onChange={handleIdentityChange} />
            合計
          </label>
        </div>

        {loading ? (
          <Oval
            height={80}
            width={80}
            color="#4fa94d"
            wrapperStyle={{}}
            wrapperClass=""
            visible={true}
            ariaLabel='oval-loading'
            secondaryColor="#4fa94d"
            strokeWidth={2}
            strokeWidthSecondary={2}
          />
        ) : error ? (
          <p>出錯了: {error.message}</p>
        ) : reversedData.length > 0 ? (
          <DataChart data={reversedData} />
        ) : (
          <p>無數據顯示</p>
        )}
      </header>
    </div>
  );
}

export default App;
