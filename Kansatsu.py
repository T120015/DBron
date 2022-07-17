from flask import Blueprint, render_template, request, session, redirect, url_for
from MyDatabase import my_open, my_query, my_close
from datetime import datetime, date
import pandas as pd

rec = Blueprint('rec', __name__)

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'testdb'  # オープンするデータベース名
}

@rec.route("/kenkou")
def kenkou():
    print(date.today())
    return render_template(
        "form_kenkou.html",
        title="健康記録",
        today = date.today()
    )


@rec.route("/kenkou1", methods=["POST"])
def kenkou1():

    code = session["id"]
    record = request.form["record"]
    meridiem = request.form["meridiem"]
    temp = request.form["temp"]
    pain = request.form["pain"]
    feeling = request.form["feeling"]
    headache = request.form["headache"]
    throat = request.form["throat"]
    breathness = request.form["breathness"]
    cough = request.form["cough"]
    nausea = request.form["nausea"]
    diarrhea = request.form["diarrhea"]
    taste = request.form["taste"]
    olfactory = request.form["olfactory"]

    dt_now = datetime.now

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        INSERT INTO kansatu
        (clientcode,record,meridiem,temp,pain,feeling,headache,
        throat,breathness,cough,nausea,diarrhea,
        taste,olfactory,lastupdate)
        VALUES
        ('{code}','{record}','{meridiem}','{temp}','{pain}','{feeling}','{headache}',
        '{throat}','{breathness}','{cough}','{nausea}','{diarrhea}',
        '{taste}','{olfactory}','{dt_now}')
        ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()

    return render_template(
        "msg.html",
        title="健康記録",
        message="健康記録を保存しました"
    )
