from mysql import connector as mydb
import sys
import pandas as pd
from MyDatabase import my_open, my_query, my_close

#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host' : 'webprog_db',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'sampledb' #オープンするデータベース名
}

#DBコネクションとカーソルを実体化
dbcon, cur = my_open(**dsn)

#sql文  f"""(ダブルコート3つ)は，複数行のf指定付きのSQL文を指定する
sqlstring = f"""
	SELECT postnumber
  FROM post_area
  WHERE prefecture = '長野県'
  AND city = '茅野市'
  ;
"""
#クエリ呼び出し
my_query(sqlstring, cur)

#クエリの結果を配列変数で読み込み
recset = pd.DataFrame(cur.fetchall())
print(recset)

#カーソルとDBコンソールのクローズ
my_close(dbcon, cur)
