import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_taifex_data(url):
    try:
        # 步驟1: 獲取HTML內容
        print("步驟1: 正在獲取網頁內容...")
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        print("網頁內容獲取成功。")

        # 步驟2: 解析HTML
        print("\n步驟2: 正在解析HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(response.text)
        print("HTML解析完成。")

        # 步驟3: 提取日期
        print("\n步驟3: 正在提取日期...")
        date_element = soup.find('span', class_='right')
        print(date_element)
        if not date_element:
            print("警告：無法找到日期元素")
            date = None
        else:
            date_str = date_element.text.strip().split('日期')[-1].strip()
            print(date_str)
            date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')
            print(f"提取的日期: {date}")

        # 步驟4: 查找表格
        print("\n步驟4: 正在查找表格...")
        tables = soup.find_all('table', class_='table_c')
        print(f"找到 {len(tables)} 個表格。")
        #print(tables)

        if len(tables) < 2:
            print(f"警告：只找到 {len(tables)} 個表格，預期至少2個")
            return date, pd.DataFrame()

        # 步驟5: 解析表格
        print("\n步驟5: 正在解析表格...")
        def parse_table(table, table_type):
            data = []
            
            rows = table.find_all('tr')[3:]  # 跳過表頭行
            print("rows : {rows}")
            for row in rows:
                cols = row.find_all(['th', 'td'])
                print("cols : {cols}")
                if len(cols) == 7:  # 確保行有正確的列數
                    identity = cols[0].text.strip()
                    row_data = [date, table_type, identity] + [col.text.strip().replace(',', '') for col in cols[1:]]
                    data.append(row_data)
                    print(f"data.append(row_data) {row_data}")
            return data

        # 解析交易數據
        trading_data = parse_table(tables[0], '交易口數與契約金額')
        print(f"解析出 {len(trading_data)} 行交易數據。")

        # 解析未平倉數據
        open_interest_data = parse_table(tables[1], '未平倉口數與契約金額')
        print(f"解析出 {len(open_interest_data)} 行未平倉數據。")

        # 步驟6: 合併數據
        print("\n步驟6: 正在合併數據...")
        all_data = trading_data + open_interest_data
        print(f"合併後總共有 {len(all_data)} 行數據。")

        # 步驟7: 創建DataFrame
        print("\n步驟7: 正在創建DataFrame...")
        columns = ['日期', '類型', '身分別', '多方口數', '多方契約金額', '空方口數', '空方契約金額', '多空淨額口數',
                   '多空淨額契約金額']
        df = pd.DataFrame(all_data, columns=columns)
        print("DataFrame創建完成。")

        # 步驟8: 轉換數值型列
        print("\n步驟8: 正在轉換數值型列...")
        numeric_columns = columns[3:]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        print("數值型列轉換完成。")

        # 打印DataFrame的基本信息
        print("\nDataFrame基本信息:")
        print(df.info())
        print("\nDataFrame前5行:")
        print(df.head())

        return date, df

    except requests.RequestException as e:
        print(f"請求錯誤：{e}")
        return None, pd.DataFrame()
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None, pd.DataFrame()

# 使用函數
url = "https://www.taifex.com.tw/cht/3/totalTableDateExcel"
date, df_result = get_taifex_data(url)

if df_result.empty:
    print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
else:
    print("\n數據獲取和處理完成。")