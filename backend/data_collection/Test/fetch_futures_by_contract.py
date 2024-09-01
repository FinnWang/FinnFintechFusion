import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def get_options_by_contract_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    print("HTTP 狀態碼:", response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取日期
    date_element = soup.find('span', class_='right')
    if date_element:
        date_str = date_element.text.strip().split('日期')[-1]
        date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')
    else:
        print("無法找到日期元素")
        date = datetime.now().strftime('%Y-%m-%d')

    # 找到表格
    table = soup.find('table', class_='table_f')
    if table is None:
        print("無法找到目標表格")
        return pd.DataFrame()
    print("找到表格，行數:", len(table.find_all('tr')))

    data = []
    current_contract = ""
    current_seq = ""
    row_count = 0

    for row in table.find_all('tr')[3:]:  # 跳過表頭行
        row_count += 1
        cols = row.find_all(['td', 'th'])
        print(f"處理第 {row_count} 行，列數: {len(cols)}")

        if len(cols) >= 15:  # 確保至少有15列
            seq = cols[0].text.strip()
            contract = cols[1].text.strip()
            if seq:
                current_seq = seq
            if contract:
                current_contract = contract
            identity = cols[2].text.strip()
            values = [col.text.strip().replace(',', '').replace('\n', '') for col in cols[3:]]

            row_data = [date, current_seq, current_contract, identity] + values
            print(f"行數據: {row_data}")

            if "小計" not in identity and "合計" not in identity:
                data.append(row_data)
                print("添加到主要數據")

    print(f"處理了 {row_count} 行數據")
    print(f"主要數據行數: {len(data)}")

    columns = ['日期', '序號', '商品名稱', '身分別',
               '多方交易口數', '多方交易契約金額', '空方交易口數', '空方交易契約金額',
               '多空交易淨額口數', '多空交易淨額契約金額',
               '多方未平倉口數', '多方未平倉契約金額', '空方未平倉口數', '空方未平倉契約金額',
               '多空未平倉淨額口數', '多空未平倉淨額契約金額']

    df = pd.DataFrame(data, columns=columns)

    # 將數值型欄位轉換為數值類型
    numeric_columns = columns[4:]
    if not df.empty:
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    print("主要數據 DataFrame 形狀:", df.shape)

    return df

# 使用函數獲取數據
url = "https://www.taifex.com.tw/cht/3/optContractsDateExcel"
df_result = get_options_by_contract_data(url)

print("\n主要數據 DataFrame 信息:")
print(df_result.info())
print("\n主要數據前5行:")
print(df_result.head())

# 生成文件名
current_date = datetime.now().strftime('%Y%m%d')
base_filename = f'options_by_contract_{current_date}.csv'

# 檢查文件是否存在，如果存在則添加時間
if os.path.exists(base_filename):
    current_time = datetime.now().strftime('%H%M%S')
    base_filename = f'options_by_contract_{current_date}_{current_time}.csv'

# 保存為 CSV 文件
df_result.to_csv(base_filename, index=False, encoding='utf-8-sig')
print(f"主要數據已成功保存為 CSV 文件：{base_filename}")

# 打印數據檢查
print("主要數據：")
print(df_result.head())
print(df_result.shape)