import React, { useState, useEffect } from 'react';
import DataChart from '../Charts/DataChart'; 
import DataFetch from '../DataTable/DataFetch';
import './Cryptocurrencies.css';

const Cryptocurrencies = () => {
    const [cryptoData, setCryptoData] = useState(null);

    useEffect(() => {
        // 從 API 獲取數據
        fetch('http://localhost:5000/api/data')
            .then(response => response.json())
            .then(data => setCryptoData(data.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
          <h2>Cryptocurrencies</h2>
          {/* 如果有數據，顯示圖表 */}
          {cryptoData ? <div className="chart-container">
                        <DataChart data={cryptoData} />
                                    </div>
                      : <p>加載中...</p>}
          
          {/* 顯示數據列表 */}
          <div className="table-container">
            <DataFetch />
          </div>
        </div>
      );
};

export default Cryptocurrencies;
