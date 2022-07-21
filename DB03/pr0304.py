import pandas as pd
import datetime
from MyDatabase import my_query, my_close, my_open
#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron03'  # オープンするデータベース名

}

dbcon, cur = my_open(**dsn)
#追加
sqlstring = f"""
    alter table seiseki
        add acunit int;
"""
my_query(sqlstring, cur)

#現在の日時を取得
dt_now = datetime.datetime.now()

i = 0  # レコード件数カウント
#ファイルオープン
df = pd.read_csv('./seiseki02.csv')
#*.csvを1行ずつ処理
for ind, rowdata in df.iterrows():

    sqlstring = f"""
        update seiseki
            set acunit = {rowdata.acunit},
            lastupdate = '{dt_now}'
            where seisekiID = {ind + 1}
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring , cur)   #1レコード挿入
    i += 1

#接続
dbcon.commit()

#カーソルとDBコンソールのクローズ
my_close(dbcon, cur)
