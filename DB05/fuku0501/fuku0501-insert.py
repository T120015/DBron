#fuku0501-insert.py
#  CSVファイルからmeiboテーブルにレコードをインポートするPythonプログラム

from MyDatabase import my_open,my_query,my_close
import pandas as pd

#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'dbron05' #オープンするデータベース名
}
dbcon,cur = my_open(**dsn)

#csvファイルオープン
df:pd.DataFrame = pd.read_csv("./fuku0501.csv",header=0)

#すべてのレコードの数だけループする
for ind, rows in df.iterrows():
    print(rows)
    sqlstring = f"""
    INSERT INTO meibo
    (gakuseki, namae, yomi, acyear, math, eng)
    VALUES(
        '{rows.gakuseki}', '{rows.namae}', '{rows.yomi}', {rows.acyear}, {rows.math}, {rows.eng}
    );
    """
    my_query(sqlstring, cur)

#DBへの書き込み
dbcon.commit()
#書き込みの確認
my_query("SELECT * FROM meibo;",cur)
recset = pd.DataFrame( cur.fetchall())
print(recset)

#DBクローズ
my_close(dbcon,cur)

