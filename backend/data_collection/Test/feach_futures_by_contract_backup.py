import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os


def get_futures_by_contract_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取日期
    date_str = soup.find('span', class_='right').text.strip().split('日期')[-1]
    date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')

    # 找到表格
    table = soup.find('table', class_='table_f')

    data = []
    current_contract = ""
    current_seq = ""

    for row in table.find_all('tr')[3:]:  # 跳過表頭行
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 13:  # 確保至少有13列（包括投信和外資的行）
            if len(cols) == 15:  # 自營商行
                seq = cols[0].text.strip()
                contract = cols[1].text.strip()
                if seq:
                    current_seq = seq
                if contract:
                    current_contract = contract
                identity = cols[2].text.strip()
                values = [col.text.strip().replace(',', '').replace('\n', '') for col in cols[3:]]
            else:  # 投信和外資行
                identity = cols[0].text.strip()
                values = [col.text.strip().replace(',', '').replace('\n', '') for col in cols[1:]]

            row_data = [date, current_seq, current_contract, identity] + values
            data.append(row_data)

    columns = ['日期', '序號', '商品名稱', '身分別',
               '多方交易口數', '多方交易契約金額', '空方交易口數', '空方交易契約金額',
               '多空交易淨額口數', '多空交易淨額契約金額',
               '多方未平倉口數', '多方未平倉契約金額', '空方未平倉口數', '空方未平倉契約金額',
               '多空未平倉淨額口數', '多空未平倉淨額契約金額']

    # 診斷信息
    print(f"列數: {len(columns)}")
    print(f"數據行數: {len(data)}")
    if data:
        print(f"第一行數據列數: {len(data[0])}")
        print(f"第一行數據: {data[0]}")

    # 確保數據與列數匹配
    data = [row[:len(columns)] for row in data]

    df = pd.DataFrame(data, columns=columns)

    # 將數值型欄位轉換為數值類型
    numeric_columns = columns[4:]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    return df


# 使用函數獲取數據
url = "https://www.taifex.com.tw/cht/3/futContractsDateExcel"
df_result = get_futures_by_contract_data(url)

# 生成文件名
current_date = datetime.now().strftime('%Y%m%d')
base_filename = f'futures_by_contract_{current_date}.csv'

# 檢查文件是否存在，如果存在則添加時間
if os.path.exists(base_filename):
    current_time = datetime.now().strftime('%H%M%S')
    filename = f'futures_by_contract_{current_date}_{current_time}.csv'
else:
    filename = base_filename

# 保存為 CSV 文件
df_result.to_csv(filename, index=False, encoding='utf-8-sig')
print(f"數據已成功保存為 CSV 文件：{filename}")

# 打印數據檢查
print(df_result.head(99))  # 顯示前15行以確保包含所有類型的行
print(df_result.shape)