# ex0402 フォームを使ってFlaskモジュールで，DBアクセス&フォームデータの受け渡し
from flask import Flask, render_template, request
from MyDatabase import my_open, my_query, my_close
import pandas as pd

# Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron04'  # オープンするデータベース名
}

# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")

# ルーティング定義


@app.route("/")
def top():
    return render_template("ex0403-top.html",
                           title="meiboテーブルメンテナンス"
                           )


@app.route("/select")
def select():
    dbcon, cur = my_open(**dsn)
    # レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT *
        FROM meibo
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template("ex0403-table.html",
                           title="meiboテーブル すべてのレコード",
                           table_data=recset
                           )


@app.route("/insert1")
def insert1():
    return render_template("ex0403-insert_form.html",
                           title="meiboテーブル レコード入力"
                           )


@app.route("/insert2", methods=["POST"])
def insert2():
    dbcon, cur = my_open(**dsn)

    # formから変数の受け取り
    namae = request.form["namae"]
    yomi = request.form["yomi"]
    spec = request.form["spec"]
    wcnt = request.form["wcnt"]

    # 更新日時取得
    import datetime
    dt_now = datetime.datetime.now()

    # レコード新規挿入のSQL文
    sqlstring = f"""
        INSERT INTO meibo
        (namae,yomi,spec,wcnt,lastupdate)
        VALUES
        ('{namae}','{yomi}',{spec},{wcnt},'{dt_now}')
        ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    message = f"{cur.rowcount}件レコードを挿入しました"

    my_close(dbcon, cur)

    return render_template("ex0403-msg.html",
                           title="レコード挿入",
                           message=message
                           )


@app.route("/update1")
def update1():
    dbcon, cur = my_open(**dsn)

    # レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT *
        FROM meibo
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    my_close(dbcon, cur)

    return render_template("ex0403-update_select.html",
                           title="meiboテーブル すべてのレコード",
                           table_data=recset
                           )


@app.route("/update2", methods=["POST"])
def update2():
    dbcon, cur = my_open(**dsn)
    meiboID = request.form["meiboID"]

    # レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT *
        FROM meibo
        WHERE meiboID = {meiboID}
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())
    # DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    rowdata = pd.Series(recset.iloc[0])

    my_close(dbcon, cur)

    return render_template("ex0403-update_form.html",
                           title=f"meiboID={meiboID} の更新",
                           table_data=rowdata
                           )


@app.route("/update3", methods=["POST"])
def update3():
    dbcon, cur = my_open(**dsn)
    meiboID = request.form["meiboID"]
    namae = request.form["namae"]
    yomi = request.form["yomi"]
    spec = request.form["spec"]
    wcnt = request.form["wcnt"]
    # 更新日時取得
    import datetime
    dt_now = datetime.datetime.now()

    # レコード更新のsql
    sqlstring = f"""
        UPDATE meibo
        SET namae = '{namae}',
            yomi = '{yomi}',
            spec = {spec},
            wcnt = {wcnt},
            lastupdate = '{dt_now}'
        WHERE meiboID = {meiboID}
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template("ex0403-msg.html",
                           title="レコード更新完了",
                           message=f"meiboID {meiboID}のレコードを更新しました"
                           )


@app.route("/delete1")
def delete1():
    dbcon, cur = my_open(**dsn)
    # meibo Table を呼出し
    sqlstring = f"""
    SELECT *
    FROM meibo
    ;
    """

    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)

    return render_template(
        "ex0403-delete_select.html",
        title="削除するレコードを選択してください",
        table_data=recset
    )


@app.route("/delete2", methods=["post"])
def delete2():
    # meiboIDの取得
    id = request.form["meiboID"]

    # 更新日時取得
    import datetime
    dt_now = datetime.datetime.now()

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        UPDATE meibo
        SET delflag = 1,
            lastupdate = '{dt_now}'
        WHERE meiboID = {id}
        """

    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "ex0403-msg.html",
        title="レコード削除フラグ",
        message=f"meiboID{id}の削除フラグを更新しました．"
    )


# プログラム起動
app.run(host="localhost", port=5000, debug=True)
