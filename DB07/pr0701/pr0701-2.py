#pr0702-2.py student.csvをDBにインポートするプログラム
from MyDatabase import my_open, my_query, my_close
from datetime import datetime as dt
import pandas as pd

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron07'
}

dbcon, cur = my_open(**dsn)

fn = "./student.csv"

dt_now = dt.now()

df: pd.DataFrame = pd.read_csv(fn, header=0)

for ind, data in df.iterrows():    
    query = f"""
        INSERT INTO student
        (s_code, namae, prefecture, lastupdate)
        VALUES
        ('{data['s_code']}','{data['namae']}','{data['prefecture']}','{dt_now}')
        ;
    """
    my_query(query, cur)

print(f"{fn}から{len(df)}レコードを新規挿入しました")
dbcon.commit()

my_close(dbcon, cur)
