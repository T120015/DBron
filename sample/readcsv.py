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

fns = [
    #"./school.csv",
    #"./client.csv", "./client2.csv",
    "./kansatu.csv", "./kansatu2.csv",
    "./koudou.csv", "./koudou2.csv"
]


def csv2df(tableName: str):
    dbcon, cur = my_open(**dsn)
    dt_now = dt.now()
    with open(fn, "r", encoding="utf-8-sig") as csv_open:
        csvfile = csv.reader(csv_open)
        for cnt, item in enumerate(csvfile):
            if cnt == 0:
                head = item

    into = ""
    for item in head:
        into += f"{item},"
    into += "lastupdate"

    df = pd.read_csv(fn, header=0)
    for ind, datas in df.iterrows():
        data = ""
        for item in datas:
            if type(item) == (int or float):
                data += f"{item},"
            else:
                data += f"'{item}',"
        data += f"'{dt_now}'"
        sql = f"""
            INSERT INTO {tableName}
            ({into})
            values
            ({data})
        """
        my_query(sql, cur)

    dbcon.commit()
    print(f"{fn}から{len(df)}レコードを新規挿入しました")

    my_close(dbcon, cur)


for i, fn in enumerate(fns):
    
    if i < 2:
        csv2df("kansatu")
    else:
        csv2df("koudou")
