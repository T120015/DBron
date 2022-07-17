from flask import Blueprint, render_template, request, session, redirect, url_for
from MyDatabase import my_open, my_query, my_close
from datetime import datetime
import pandas as pd

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron'  # オープンするデータベース名
}

cnt = Blueprint('cnt', __name__)


@cnt.route("/")
def top():
    # トップページ
    return render_template(
        "top.html", title="メインメニュー", msg="main src", school=session["school"]
    )


@cnt.route("/coronakansenn")
def kannsenn():
    return render_template(
        "coronakansenn.html",
        title="コロナ感染した人用"
    )


@cnt.route("/coronakansenn1", methods=["POST"])
def kannsenn1():
    clientcode = request.form["clientcode"]
    coronakansennbi = request.form["coronakansennbi"]
    kansenn = request.form["kansenn"]
    dt_now = datetime.now

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        INSERT INTO corona
        (clientcode,judge,onset,lastupdate)
        VALUES
        ('{clientcode}','{kansenn}','{coronakansennbi}','{dt_now}')
        ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)
    return render_template(
        "msg.html",
        title="コロナ感染者or濃厚接触者",
        message="を保存しました"
    )
