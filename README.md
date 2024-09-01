Todo
_期貨契約_網頁原始檔案
https://www.taifex.com.tw/cht/3/futContractsDateExcel

_期貨大額交易人未沖銷部位結構表_網頁原始檔案
https://www.taifex.com.tw/cht/3/largeTraderFutQryTbl

三大法人-總表
https://www.taifex.com.tw/cht/3/totalTableDateExcel

三大法人-區分各期貨契約
https://www.taifex.com.tw/cht/3/futContractsDateExcel


我的目的是透過爬蟲蒐集台灣股市的盤後數據，數據包含股票`期貨`選擇權`等等資訊.詳細內容我還須要想一下

但目的是會有一個響應式的前端介面,讓我每日可以執行這個程式.並開始蒐集資料.並透過一個簡易的互動式介面,可以視覺化的呈現今日與昨日的比較,以及這周的股市籌碼變化

關於響應式的前端介面與簡易的互動式介面以及視覺化的呈現  有哪些工具可以使用

我目前只有使用過Pycharm與Python 我不排斥其他語言以及使用其他的平台(例如Visual code) 請給我好的建議


資料蒐集與處理 : Python
Dataabase : PostgreSQL(備選 : SQLite)
後端框架 : Flask
前端框架 : React + ChartJS
數據可視化 : ""Plotly" / D3.js / Chart.js (我想要搭配互動式做交互) 該如何選擇



1.
![alt text](image.png)
2. 資料夾的詳細說明
components/:

存放所有可重用的 React 組件。這些組件通常是無狀態（stateless）的，但也可以包含部分狀態邏輯。
例如：DataChart.js 用於展示圖表，DataFetch.js 用於數據獲取等。
hooks/:

存放所有自定義的 React Hook。這些 Hook 封裝了複雜的邏輯，可以在多個組件中重用。
例如：useCycleDates.js 封裝了日期計算的邏輯。
utils/:

存放各種輔助函數或模組，這些函數通常與特定業務無關，僅用於簡化邏輯。
例如：dateUtils.js 可以存放日期操作相關的函數。
pages/:

存放頁面級別的組件。這些組件通常是應用的主要路由入口。
例如：HomePage.js 是應用的主頁組件。
services/:

存放與業務邏輯相關的代碼，如 API 請求、資料存取等。這些服務層的代碼通常與具體的 UI 無關。
例如：api.js 可以封裝所有與後端交互的 API 請求。