#q23-[GAKUSEKI].py  CSVファイルをテーブルにインポートするプログラム

from MyDatabase import my_open, my_query, my_close
from datetime import datetime as dt
import pandas as pd

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbtest01'
}

dbcon, cur = my_open(**dsn)

fn = "./uriage.csv"

dt_now = dt.now()

df: pd.DataFrame = pd.read_csv(fn, header=0)

for ind, data in df.iterrows():    
    query = f"""
        INSERT INTO uriage
        (tantou, area, sales, s_date, lastupdate)
        VALUES
        ('{data['tantou']}','{data['area']}',{data['sales']},'{data['s_date']}','{dt_now}')
        ;
    """
    my_query(query, cur)

print(f"{fn}から{len(df)}レコードを新規挿入しました")
dbcon.commit()

my_close(dbcon, cur)

