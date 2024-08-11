import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

#Source
#https://www.taifex.com.tw/cht/3/totalTableDateExcel
def get_taifex_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果請求不成功則拋出異常
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取日期
        date_element = soup.find('span', class_='right')
        if not date_element:
            print("警告：無法找到日期元素")
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = date_element.text.strip().split('日期')[-1]
            date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')

        # 找到所有表格
        tables = soup.find_all('table', class_='table_c')
        if len(tables) < 2:
            print(f"警告：只找到 {len(tables)} 個表格，預期至少2個")
            return pd.DataFrame()  # 返回空的DataFrame

        def parse_table(table, table_type):
            data = []
            rows = table.find_all('tr')[3:]  # 跳過表頭行
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) == 7:  # 確保行有正確的列數
                    identity = cols[0].text.strip()
                    row_data = [date, table_type, identity] + [col.text.strip().replace(',', '') for col in cols[1:]]
                    data.append(row_data)
            return data

        # 解析交易數據
        trading_data = parse_table(tables[0], '交易口數與契約金額')

        # 解析未平倉數據
        open_interest_data = parse_table(tables[1], '未平倉口數與契約金額')

        # 合併數據
        all_data = trading_data + open_interest_data

        # 創建DataFrame
        columns = ['日期', '類型', '身分別', '多方口數', '多方契約金額', '空方口數', '空方契約金額', '多空淨額口數',
                   '多空淨額契約金額']
        df = pd.DataFrame(all_data, columns=columns)

        # 轉換數值型列
        numeric_columns = columns[3:]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return df

    except requests.RequestException as e:
        print(f"請求錯誤：{e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"發生錯誤：{e}")
        return pd.DataFrame()


# 使用函數獲取數據
url = "https://www.taifex.com.tw/cht/3/totalTableDateExcel"
df_result = get_taifex_data(url)

if df_result.empty:
    print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
else:
    # 打印數據檢查
    print(df_result)

    # 生成文件名
    current_date = datetime.now().strftime('%Y%m%d')
    base_filename = f'processed_taifex_data_{current_date}.csv'

    # 檢查文件是否存在，如果存在則添加時間
    if os.path.exists(base_filename):
        current_time = datetime.now().strftime('%H%M%S')
        filename = f'processed_taifex_data_{current_date}_{current_time}.csv'
    else:
        filename = base_filename

    # 保存為 CSV 文件
    try:
        df_result.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"數據已成功保存為 CSV 文件：{filename}")
    except PermissionError:
        print(f"無法保存文件 {filename}。請確保文件未被其他程序打開。")
    except Exception as e:
        print(f"保存文件時發生錯誤：{e}")