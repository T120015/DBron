from MyDatabase import my_open, my_query, my_close
from datetime import datetime as dt
import pandas as pd
import csv

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron'
}


def csv2df(fd):
    print(type(fd))
    dbcon, cur = my_open(**dsn)
    dt_now = dt.now()
    
    df = pd.read_csv(fd, header=0)
    into = ""
    for item in df.columns:
        into += f"{item},"
    into += "lastupdate"
    
    for ind, datas in df.iterrows():
        data = ""
        for item in datas:
            if type(item) == (int or float):
                data += f"{item},"
            else:
                data += f"'{item}',"
        data += f"'{dt_now}'"
        sql = f"""
            INSERT INTO client
            ({into})
            values
            ({data})
        """
        my_query(sql, cur)

    dbcon.commit()
    my_close(dbcon, cur)
    return f"{fd.filename}から{len(df)}レコードを新規挿入しました"

