# pr0603.py
from MyDatabase import my_open , my_query , my_close
import pandas as pd

#Data Source Nameのパラメータを辞書型変数で定義しオープン
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'dbron06' #オープンするデータベース名
}

from flask import Flask,render_template ,request
#Flaskのコンストラクタ
app = Flask(__name__ ,static_folder="static")

@app.route("/")
def index():
    dbcon, cur = my_open(**dsn)
    query = f"""
        SELECT DISTINCT cname
        FROM item_cus_sal
        ;
    """
    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    
    return render_template(
        "pr0603-top.html",
        title = "文房具注文確認",
        table_data = recset
    )

@app.route("/total1")
def total1():
    dbcon, cur = my_open(**dsn)
    query = f"""
        select cname, sum(price) as totalprice
        from item_cus_sal
        group by cname
        ;
    """
    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "pr0603-table.html",
        title = "文具注文の集計結果",
        table_data = recset,
        flag = 0
    )

@app.route("/total2", methods=['POST'])
def total2():
    cname = request.form['cname']
    flag = 1 if request.form.getlist('flag') else 0
    dbcon, cur = my_open(**dsn)
    query = f"""
        select *
        from item_cus_sal
        where cname = '{cname}'
        ;
    """
    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_columns', None)
    
    return render_template(
        "pr0603-table.html",
        title = f"{cname}の集計結果",
        table_data=recset.loc[:, 'cname':],
        flag = flag
    )

app.run('127.0.0.1', 5000, True)
