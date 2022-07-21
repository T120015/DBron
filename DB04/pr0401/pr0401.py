# pr0401　Flaskモジュールで，DBアクセス&データ分析
from flask import Flask, render_template, request
from crypt import methods
from numpy import rec
from MyDatabase import my_open, my_query, my_close
import pandas as pd

# Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'sampledb'  # オープンするデータベース名
}

# flaskモジュールのインポートと実体化 <== お決まり
app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    dbcon, cur = my_open(**dsn)

    sqlstr = f"""
    SELECT DISTINCT prefecture
    FROM quest
    ;
    """

    my_query(sqlstr, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    # print(recset)

    return render_template(
        "pr0401-top.html",
        title="アンケート回答者の都道府県名",
        table_data=recset
    )


@app.route("/search", methods=["POST"])
def table():
    prefecture = request.form["prefecture"]

    dbcon, cur = my_open(**dsn)
    sqlstr = f"""
    SELECT *
    FROM quest
    WHERE prefecture = '{prefecture}'
    """

    my_query(sqlstr, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)

    return render_template(
        "pr0401-table.html",
        title=f"{prefecture}のアンケート一覧",
        table_data=recset
    )


# プログラム起動
app.run(host="localhost", port=5000, debug=True)
