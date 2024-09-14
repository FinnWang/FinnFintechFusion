from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class TaifexFuturesContractsData(Base):
    __tablename__ = 'taifex_futures_contracts_data'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    serial = Column(Integer)
    product = Column(String)
    identity = Column(String)
    long_position = Column(Integer)
    long_amount = Column(Float)
    short_position = Column(Integer)
    short_amount = Column(Float)
    net_position = Column(Integer)
    net_amount = Column(Float)
    open_interest_long_position = Column(Integer)
    open_interest_long_amount = Column(Float)
    open_interest_short_position = Column(Integer)
    open_interest_short_amount = Column(Float)
    open_interest_net_position = Column(Integer)
    open_interest_net_amount = Column(Float)

    __table_args__ = (UniqueConstraint('date', 'serial', 'product', 'identity', name='uix_futures_contracts'),)

def get_taifex_futures_contracts_data(url):
    try:
        # 使用 Selenium 進行網頁抓取
        chrome_options = Options()
        # 暫時註解掉無頭模式
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')

        # 設定 ChromeDriver 的路徑
        service = Service('C:\Finn\Git\chromedriver-win64\chromedriver.exe')  # 替換為你的 chromedriver.exe 的實際路徑
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        
        # 顯式等待，直到表格出現
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "table_f"))
        )

        # 獲取網頁的 HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()  # 關閉瀏覽器

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

    except Exception as e:
        print(f"發生錯誤：{e}")
        return None, pd.DataFrame()

def save_to_csv(df, web_date, target_dir):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'taifex_futures_contracts_data_{web_date}_{current_datetime}.csv'
    full_path = os.path.join(target_dir, filename)
    df.to_csv(full_path, index=False, encoding='utf-8-sig')
    print(f"數據已保存為CSV: {full_path}")

def save_to_postgres(df, engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _, row in df.iterrows():
            data = TaifexFuturesContractsData(
                date=row['日期'],
                serial=row['序號'],
                product=row['商品名稱'],
                identity=row['身分別'],
                long_position=row['多方口數'],
                long_amount=row['多方金額'],
                short_position=row['空方口數'],
                short_amount=row['空方金額'],
                net_position=row['多空淨口數'],
                net_amount=row['多空淨額'],
                open_interest_long_position=row['未平倉多方口數'],
                open_interest_long_amount=row['未平倉多方金額'],
                open_interest_short_position=row['未平倉空方口數'],
                open_interest_short_amount=row['未平倉空方金額'],
                open_interest_net_position=row['未平倉淨口數'],
                open_interest_net_amount=row['未平倉淨額']
            )
            session.add(data)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                print(f"跳過重複數據: 日期 {row['日期']}, 序號 {row['序號']}, 商品名稱 {row['商品名稱']}, 身分別 {row['身分別']}")

        print("數據已成功保存到 PostgreSQL 數據庫")
    except Exception as e:
        session.rollback()
        print(f"保存到 PostgreSQL 數據庫時發生錯誤：{e}")
    finally:
        session.close()

# 主程序
if __name__ == "__main__":
    url = "https://www.taifex.com.tw/cht/3/futContractsDateExcel"
    web_date, df_result = get_taifex_futures_contracts_data(url)

    if df_result.empty:
        print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
    else:
        # 設置 PostgreSQL 連接
        # 請替換以下連接字符串中的用戶名、密碼、主機和數據庫名稱
        engine = create_engine('postgresql://postgres:5432@localhost:5432/NewDB')
        Base.metadata.create_all(engine)

        # 保存到 PostgreSQL
        save_to_postgres(df_result, engine)

        # 保存為CSV
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # target_dir = os.path.abspath(os.path.join(current_dir, '..', 'datarecord'))
        # os.makedirs(target_dir, exist_ok=True)
        # save_to_csv(df_result, web_date, target_dir)
