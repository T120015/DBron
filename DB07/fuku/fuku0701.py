#fuku0701.py 
#FlaskモジュールでDBの操作
from MyDatabase import my_open , my_query , my_close
import pandas as pd

#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'sampledb' #オープンするデータベース名
}

from flask import Flask,render_template ,request
#Flaskのコンストラクタ
app = Flask(__name__ ,static_folder="static")

#ルーティング定義
@app.route("/")
def top():
    return render_template( "fuku0701-top.html",
        title = "Fuku0701トップ" 
    )

@app.route("/goukei1")
def goukei1():
    #n入力
    dbcon, cur = my_open(**dsn)
    query = f"""
        SELECT s_id, s_name, SUM(s_value) AS goukei
        FROM shop_sales
        GROUP BY s_id
        ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "fuku0701-table.html",
        title = "店舗ごとの集計結果",
        table_data = recset
    )


@app.route("/goukei2")
def goukei2():
    #n入力
    dbcon, cur = my_open(**dsn)
    query = f"""
        SELECT s_date, SUM(s_value) AS goukei
        FROM shop_sales
        GROUP BY s_date
        ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "fuku0701-table.html",
        title="売り上げごとの集計結果",
        table_data=recset
    )

#プログラム起動
app.run(host="localhost",port=5000,debug=True)
