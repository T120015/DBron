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

#テーブルを作成する。
my_query("DROP TABLE if EXISTS seiseki;", cur)
sqlstring = f"""
    CREATE TABLE seiseki(
        seisekiID int not null auto_increment,
        gakuseki varchar(16) not null,
        namae varchar(32) not null,
        gpa float,
        gps float,
        lastupdate varchar(128) not null,
        primary key(seisekiID)
    );
"""
my_query(sqlstring, cur)

#現在の日時を取得
dt_now = datetime.datetime.now()

i = 0  # レコード件数カウント
#ファイルオープン
df = pd.read_csv('./seiseki01.csv')
#weather.csvを1行ずつ処理
for ind, rowdata in df.iterrows():

    sqlstring = f"""
        INSERT INTO seiseki
        (gakuseki, namae, gpa, gps, lastupdate)
        VALUES
        ('{rowdata[0]}','{rowdata[1]}',{rowdata[2]},{rowdata[3]},'{dt_now}' )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring , cur)   #1レコード挿入
    i += 1

#接続
dbcon.commit()
#テーブル構造の表示
my_query("DESC seiseki", cur)
print("result: DESC seiseki;")
for col in cur:
    print(col)

#カーソルとDBコンソールのクローズ
my_close(dbcon, cur)
