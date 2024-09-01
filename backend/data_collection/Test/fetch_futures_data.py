import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def get_taifex_futures_contracts_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取日期
        date_element = soup.find('span', class_='right')
        if not date_element:
            print("警告：無法找到日期元素")
            return None, pd.DataFrame()
        date_str = date_element.text.strip().split('日期')[-1].strip()
        date = datetime.strptime(date_str, '%Y/%m/%d').date()

        # 找到主要數據表格
        table = soup.find('table', class_='table_f')
        if not table:
            print("警告：無法找到數據表格")
            return date, pd.DataFrame()

        data = []
        current_serial = None
        current_product = None
        rows = table.find_all('tr')[3:]  # 跳過表頭行

        for i in range(0, len(rows), 3):  # 每三行為一組數據
            if i + 2 >= len(rows):
                break

            cells_1 = rows[i].find_all(['td', 'th'])
            cells_2 = rows[i+1].find_all(['td', 'th'])
            cells_3 = rows[i+2].find_all(['td', 'th'])

            if len(cells_1) == 15 and cells_1[0].get('rowspan') == '3':
                current_serial = int(cells_1[0].text.strip())
                current_product = cells_1[1].text.strip()

                if current_product == '期貨小計':
                    break

                # 自營商
                row_data = [date, current_serial, current_product, '自營商'] + [cell.text.strip().replace(',', '') for cell in cells_1[3:]]
                data.append(row_data)

                # 投信
                row_data = [date, current_serial, current_product, '投信'] + [cell.text.strip().replace(',', '') for cell in cells_2[1:]]
                data.append(row_data)

                # 外資
                row_data = [date, current_serial, current_product, '外資'] + [cell.text.strip().replace(',', '') for cell in cells_3[1:]]
                data.append(row_data)

        # 創建DataFrame
        columns = ['日期', '序號', '商品名稱', '身分別', 
                   '多方口數', '多方金額', '空方口數', '空方金額', '多空淨口數', '多空淨額',
                   '未平倉多方口數', '未平倉多方金額', '未平倉空方口數', '未平倉空方金額', '未平倉淨口數', '未平倉淨額']
        df = pd.DataFrame(data, columns=columns)

        # 轉換數值型列
        numeric_columns = columns[4:]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return date, df

    except requests.RequestException as e:
        print(f"請求錯誤：{e}")
        return None, pd.DataFrame()
    except Exception as e:
        print(f"發生錯誤：{e}")
        return None, pd.DataFrame()

# 主程序
if __name__ == "__main__":
    url = "https://www.taifex.com.tw/cht/3/futContractsDateExcel"
    web_date, df_result = get_taifex_futures_contracts_data(url)

    if df_result.empty:
        print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
    else:
        # 保存為CSV
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'datarecord'))
        os.makedirs(target_dir, exist_ok=True)
        csv_filename = f'processed_taifex_futures_contracts_data_{web_date}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        full_path = os.path.join(target_dir, csv_filename)
        df_result.to_csv(full_path, index=False, encoding='utf-8-sig')
        print(f"數據已保存為CSV: {full_path}")