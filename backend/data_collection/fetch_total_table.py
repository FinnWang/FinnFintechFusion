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
            date = None
        else:
            date_str = date_element.text.strip().split('日期')[-1].strip()
            date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')

        # 找到所有表格
        tables = soup.find_all('table', class_='table_c')
        if len(tables) < 2:
            print(f"警告：只找到 {len(tables)} 個表格，預期至少2個")
            return date, pd.DataFrame()

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

        return date, df

    except requests.RequestException as e:
        print(f"請求錯誤：{e}")
        return None, pd.DataFrame()
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None, pd.DataFrame()

# 使用函數獲取數據
url = "https://www.taifex.com.tw/cht/3/totalTableDateExcel"
web_date, df_result = get_taifex_data(url)

if df_result.empty:
    print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
else:
    # 打印數據檢查
    print(df_result)

    # 獲取當前腳本的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 構建到 datarecord 目錄的路徑
    target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'datarecord'))

    # 確保目標目錄存在
    os.makedirs(target_dir, exist_ok=True)

    # 獲取當前日期和時間
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 使用網頁中的日期和當前日期時間生成文件名
    if web_date:
        filename = f'processed_taifex_data_{web_date}_{current_datetime}.csv'
    else:
        filename = f'processed_taifex_data_unknown_{current_datetime}.csv'

    full_path = os.path.join(target_dir, filename)

    # 保存為 CSV 文件
    try:
        df_result.to_csv(full_path, index=False, encoding='utf-8-sig')
        print(f"數據已成功保存為 CSV 文件：{full_path}")
    except PermissionError:
        print(f"無法保存文件 {full_path}。請確保文件未被其他程序打開。")
    except Exception as e:
        print(f"保存文件時發生錯誤：{e}")