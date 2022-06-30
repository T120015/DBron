# q32

# q23-[GAKUSEKI].py  CSVファイルをテーブルにインポートするプログラム

import datetime
from MyDatabase import my_open, my_query, my_close
import pandas as pd

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbtest01'
}
dbcon, cur = my_open(**dsn)

filename = ["./gakuseki.csv", "./kamoku.csv", "./attendance.csv"]

dt_now = datetime.datetime.now()

for fn in filename:
    df = pd.read_csv(fn, header=0)

    for ind, rowdata in df.iterrows():
        if fn == filename[0]:
            sqlstring = f"""
                INSERT INTO gakuseki
                (gakusekicode,namae,a_year,lastupdate)
                values
                ('{rowdata.gakusekicode}','{rowdata.namae}','{rowdata.a_year}','{dt_now}')
                ;
            """
        elif fn == filename[1]:
            sqlstring = f"""
                INSERT INTO kamoku
                (kamokucode, subjectname, tantou, lastupdate)
                values
                ('{rowdata.kamokucode}','{rowdata.subjectname}','{rowdata.tantou}','{dt_now}')
            """

        else:
            sqlstring = f"""
                INSERT INTO attendance
                (gakusekicode,kamokucode,classdate,atdata,lastupdate)
                values
                ('{rowdata.gakusekicode}','{rowdata.kamokucode}','{rowdata.classdate}','{rowdata.atdata}','{dt_now}')
                ;
            """

        my_query(sqlstring, cur)

    print(f"{fn}を{len( df )}レコードを新規挿入しました")

    dbcon.commit()

my_close(dbcon, cur)
