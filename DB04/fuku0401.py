from scipy.stats import chi2_contingency
import datetime
from MyDatabase import my_open, my_query, my_close
import pandas as pd

# Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': ''  # オープンするデータベース名
}
dbcon, cur = my_open(**dsn)

# (1) DB新規作成
my_query("CREATE DATABASE if not EXISTS dbron04;", cur)
my_query("USE dbron04;", cur)

# (2)テーブル新規作成
my_query("DROP TABLE if EXISTS naitei;", cur)
sqlstring = f"""
    CREATE TABLE naitei(
        naiteiID int not NULL auto_increment,
        gakuseki varchar(10),
        namae varchar(30),
        job varchar(10),
        gender varchar(30),
        club varchar(10),
        lastupdated datetime,
        primary key (naiteiID)
    )
    ;
"""
my_query(sqlstring, cur)
# テーブルの説明
my_query("DESC naitei;", cur)
# 結果の表示
recset = pd.DataFrame(cur.fetchall())
print(recset)

# (3)CSVファイルのインポート
dt_now = datetime.datetime.now()

# ファイルオープン
df = pd.read_csv("./naitei.csv", header=0)
# weather.csvを1行ずつ処理
for ind, rowdata in df.iterrows():

    sqlstring = f"""
        INSERT INTO naitei
        (gakuseki,namae, job, gender, club , lastupdated)
        VALUES
        ('{rowdata.gakuseki}','{rowdata.namae}',
        '{rowdata.job}','{rowdata.gender}','{rowdata.club}',
        '{dt_now}' )
        ;
    """
    # print( sqlstring )  #for debug
    my_query(sqlstring, cur)  # 1レコード挿入
# DBに書き込み

print(f"naiteiテーブル{len(df)} レコード追加しました")

# (4)
sqlstring = f"""
    SELECT *
    FROM naitei
    WHERE gakuseki BETWEEN 'H010' AND 'H015'
    ;
"""
my_query(sqlstring, cur)
recset = pd.DataFrame(cur.fetchall())
print(recset)

# (5)
sqlstring = f"""
    SELECT *
    FROM naitei
    ;
"""
my_query(sqlstring, cur)
recset = pd.DataFrame(cur.fetchall())

ctable = pd.crosstab(recset.job, recset.gender)
print(ctable)

# (6)
# correaction=False イエーツの補正を行わない<==一般的
result = chi2_contingency(ctable, correction=False)
# print(result)

print(f"カイ二乗値は {result[0]}")
print(f"確率は {result[1]} ")
print(f"自由度は {result[2]}")
print(f"期待度数 {result[3]}")

if result[1] < 0.05:
    print("有意な差があります")
else:
    print("有意な差がありません")

# dbクローズ
my_close(dbcon, cur)
