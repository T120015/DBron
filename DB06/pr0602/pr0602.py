#pr0602.py 3つのCSVファイルをテーブルにインポートするプログラム
from MyDatabase import my_open, my_query, my_close
from datetime import datetime as dt
import pandas as pd

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron06'
}

dbcon, cur = my_open(**dsn)

file_name = ["./pr0602-item.csv", "./pr0602-customer.csv", "./pr0602-salesdetail.csv"]

dt_now = dt.now()

for fn in file_name:
    df: pd.DataFrame = pd.read_csv(fn, header=0)

    for ind, data in df.iterrows():
        if fn == "./pr0602-item.csv":
            query = f"""
                INSERT INTO item
                (itemcode, iname, unitprice, maker, lastupdate)
                VALUES
                ('{data['itemcode']}','{data['iname']}',{data['unitprice']},'{data['maker']}','{dt_now}')
                ;
            """
        elif fn == "./pr0602-customer.csv":
            query = f"""
                INSERT INTO customer
                (cname, caddress, tel, lastupdate)
                VALUES
                ('{data['cname']}','{data['caddress']}','{data['tel']}','{dt_now}')
                ;
            """
        else:
            query =  f"""
                INSERT INTO salesdetail
                (itemcode, customerID, quantity, salesdate, lastupdate)
                VALUES
                ('{data['itemcode']}', {data['customerID']}, {data['quantity']}, '{data['salesdate']}', '{dt_now}')
                ;
            """
        
        my_query(query,cur)
    
    print(f"{fn}から{len(df)}レコードを新規挿入しました")
    dbcon.commit()

my_close(dbcon, cur)
