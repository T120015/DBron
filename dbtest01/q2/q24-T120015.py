#q24-[GAKUSEKI].py 
#FlaskモジュールでDBの操作

from crypt import methods
from flask import Flask, render_template, request
import pandas as pd
from MyDatabase import my_open, my_query, my_close
from datetime import datetime as dt

from sympy import true

app = Flask(__name__, static_folder="static")


dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbtest01'
}


@app.route("/")
def top():
    return render_template(
        "top.html",
        title = "売り上げ管理DB"
    )


@app.route("/select_all")
def select_all():
    dbcon, cur = my_open(**dsn)
    query = f"""    
    SELECT *
    FROM uriage
    where cancelflag = 0
    ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    return render_template(
        "table.html",
        title = "全てのレコード一覧表示",
        table_data = recset
    )


@app.route("/tantou1")
def tantou1():
    dbcon, cur = my_open(**dsn)
    query = f"""
        SELECT DISTINCT tantou
        FROM uriage
        where cancelflag = 0
        ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    return render_template(
        "form.html",
        title = "担当者選択画面",
        msg = "担当者を選択してください",
        table_data = recset['tantou']
    )

@app.route("/tantou2", methods=["post"])
def tantou2():
    tantou = request.form['tantou']

    dbcon, cur = my_open(**dsn)
    query = f"""
            SELECT *
            FROM uriage
            where tantou = "{tantou}"
            and cancelflag = 0
            ;
        """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    return render_template(
        "table.html",
        title = f"担当者: {tantou}の打ち上げ一覧",
        table_data = recset
    )


@app.route("/update_cancel1")
def update1():

    dbcon, cur = my_open(**dsn)
    query = f"""    
    SELECT *
    FROM uriage
    where cancelflag = 0
    ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)

    return render_template(
        "update.html",
        title = "キャンセルレコード選択画面",
        table_data = recset
    )


@app.route("/update_cancel2", methods=['post'])
def update2():
    id = request.form['uriageID']

    dbcon, cur = my_open(**dsn)
    query = f"""    
    SELECT *
    FROM uriage
    where cancelflag = 0
    and uriageid = {id}
    ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    print(recset)
    return render_template(
        "cancel.html",
        title=f"uriageID: {id}のキャンセル処理",
        data=recset
    )

@app.route("/update_cancel3", methods=["post"])
def update3():
    id = request.form['uriageID']

    dt_now = dt.now()
    dbcon, cur = my_open(**dsn)
    query = f"""
        update uriage
        set cancelflag = 1,
            lastupdate = '{dt_now}'
        where uriageID = {id}
        ;
    """

    my_query(query, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "msg.html",
        title = f"レコード削除",
        msg = f"uriageID: {id}のレコードを削除しました．"
    )

@app.route("/pivot")
def pivot():

    dbcon, cur = my_open(**dsn)
    query = f"""
        select *
        from uriage
        where cancelflag = 0
        ;
    """

    my_query(query, cur)
    recset = pd.DataFrame(cur.fetchall())
    data = recset.loc[:,'tantou':'sales']
    result = pd.pivot_table(data, index='tantou', columns='area', aggfunc=sum, margins=true)

    return render_template(
        "pivot.html",
        title = f"担当者ｘ地域の集計結果",
        table_data = result
    )

app.run("localhost", 5000, True)