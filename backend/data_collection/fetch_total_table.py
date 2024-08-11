import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class TaifexData3Total(Base):
    __tablename__ = 'taifex_data_3total'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    data_type = Column(String)
    identity = Column(String)
    long_position = Column(Integer)
    long_amount = Column(Float)
    short_position = Column(Integer)
    short_amount = Column(Float)
    net_position = Column(Integer)
    net_amount = Column(Float)

    # 添加唯一約束，以防止重複數據
    __table_args__ = (UniqueConstraint('date', 'data_type', 'identity', name='uix_1'),)

def get_taifex_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
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

def save_to_csv(df, target_dir, web_date):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    if web_date:
        filename = f'processed_taifex_data_{web_date}_{current_datetime}.csv'
    else:
        filename = f'processed_taifex_data_unknown_{current_datetime}.csv'

    full_path = os.path.join(target_dir, filename)

    try:
        df.to_csv(full_path, index=False, encoding='utf-8-sig')
        print(f"數據已成功保存為 CSV 文件：{full_path}")
    except Exception as e:
        print(f"保存 CSV 文件時發生錯誤：{e}")

def save_to_postgres(df, engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _, row in df.iterrows():
            data = TaifexData3Total(
                date=row['日期'],
                data_type=row['類型'],
                identity=row['身分別'],
                long_position=row['多方口數'],
                long_amount=row['多方契約金額'],
                short_position=row['空方口數'],
                short_amount=row['空方契約金額'],
                net_position=row['多空淨額口數'],
                net_amount=row['多空淨額契約金額']
            )
            session.add(data)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                print(f"跳過重複數據: 日期 {row['日期']}, 類型 {row['類型']}, 身分別 {row['身分別']}")

        print("數據已成功保存到 PostgreSQL 數據庫")
    except Exception as e:
        session.rollback()
        print(f"保存到 PostgreSQL 數據庫時發生錯誤：{e}")
    finally:
        session.close()

# 主程序
if __name__ == "__main__":
    url = "https://www.taifex.com.tw/cht/3/totalTableDateExcel"
    web_date, df_result = get_taifex_data(url)

    if df_result.empty:
        print("無法獲取數據，請檢查網絡連接或網頁結構是否發生變化。")
    else:
        # 設置 PostgreSQL 連接
        # 請替換以下連接字符串中的用戶名、密碼、主機和數據庫名稱
        engine = create_engine('postgresql://postgres:5432@localhost:5432/NewDB')
        Base.metadata.create_all(engine)

        # 保存到 PostgreSQL
        save_to_postgres(df_result, engine)

        # 保存到 CSV（保留但不使用）
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'datarecord'))
        # os.makedirs(target_dir, exist_ok=True)
        # save_to_csv(df_result, target_dir, web_date)