from flask import Blueprint, render_template, request, redirect, url_for, session
from MyDatabase import my_open, my_query, my_close
import pandas as pd
from datetime import datetime, date, timedelta
from Read_csv import csv2df

mng = Blueprint('mng', __name__, url_prefix='/manage')

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron'  # オープンするデータベース名
}


@mng.before_request
def checkManager():
    if session["school"] < 7:
        return render_template(
            "msg.html",
            title="アクセスできません",
            msg="このアカウントは管理者権限がありません."
        )


@mng.route("/")
def manage():
    # 管理者メニュー
    return render_template(
        "manage.html",
        title="管理者メニュー"
    )


@mng.route("/table")
def table():
    dbcon, cur = my_open(**dsn)
    sql = f"""
        select *
        from acount
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "table.html",
        title="関係者一覧",
        table_data=recset.loc[:, 'clientcode':].sort_values('clientcode')
    )


@mng.route("/insert")
def insert():
    dbcon, cur = my_open(**dsn)
    sql = f"""
        select distinct position
        from school
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    position = list(recset['position'])

    sql = f"""
        select class
        from school
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    cls = list(recset['class'])
    my_close(dbcon, cur)

    return render_template(
        "form_input.html",
        title="関係者追加",
        input_position=position,
        input_class=cls,
        url="/",
        to_url="/insert1",
        position="",
        cls=""
    )


@mng.route("/insert_files")
def insert_files():
    return render_template(
        "form_files.html",
        title="関係者追加"
    )


@mng.route("/insert_files1")
def insert_files1():
    # csvFileの受け取り
    csv_file = request['upfile']
    msg = csv2df(csv_file)

    return render_template(
        "msg.html",
        title="追加完了",
        msg=msg
    )


@mng.route("/update")
def update():
    dbcon, cur = my_open(**dsn)
    sql = f""""
        select *
        from acount
        ;
    """
    return render_template(
        "select.html",
        title="関係者情報編集",
        table_data=table
    )


@mng.route("/update1", methods=['post'])
def update1():
    code = request.form['clientcode']
    dbcon, cur = my_open(**dsn)
    sql = f"""
        select distinct position
        from school
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    position = list(recset['position'])

    sql = f"""
        select class
        from school
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    cls = list(recset['class'])

    sql = f"""
        select *
        from acount
        where clientcode = '{code}'
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    print(recset["namae"])
    return render_template(
        "form_input.html",
        title=f"{code}の編集",
        input_position=position,
        input_class=cls,
        url="/update",
        to_url="/update2",
        name=recset["namae"][0],
        gender=recset["gender"][0],
        age=recset["age"][0],
        phone=recset["phone"][0],
        email=recset["email"][0],
        faculty=recset["faculty"][0],
        position=recset["position"][0],
        cls=recset["class"][0]
    )


@mng.route("/delete")
def delete():

    return render_template(
        "select.html",
        title="関係者情報削除"
    )


# manage テーブル表示
@mng.route("/kirokunasi")
def kirokunasi():

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        SELECT *
        FROM kansatu
        left outer JOIN client
        on kansatu.clientcode = client.clientcode
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    li = list()
    delta = timedelta(days=3)
    for item in recset.values:
        debug = date.today() - item[2]
        if debug > delta:
            li.append(item[1])

    li = pd.DataFrame(li, columns=['clientcode'])
    print(li)

    return render_template("table.html",
                           title="3日以上連続記録なし",
                           table_data=li
                           )


@mng.route("/kaityou")
def kaityou():

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        SELECT *
        FROM kansatu
        left outer JOIN client
        on kansatu.clientcode = client.clientcode
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)

    li = list()
    for item in recset.values:
        flag = 0
        for ck in item:
            if type(ck) == int:
                flag += ck
        if item[4] > 37.5 or flag:
            li.append(item[1])

    li = pd.DataFrame(li, columns=['clientcode'])

    return render_template("table.html",
                           title="37.5度以上or5個チェックの人",
                           table_data=li
                           )


@mng.route("/korona")
def korona():

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        SELECT client.clientcode,faculty,namae,phone,email,onset,stopflag,corona.lastupdate,corona.delflag
        FROM corona
        INNER JOIN client
        ON corona.clientcode = client.clientcode
        WHERE judge = 'True'
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template("table.html",
                           title="コロナ感染者",
                           table_data=recset
                           )


@mng.route("/noukousessyoku")
def noukousessyoku():

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        SELECT client.clientcode,faculty,namae,phone,email,onset,stopflag,corona.lastupdate,corona.delflag
        FROM corona
        INNER JOIN client
        ON corona.clientcode = client.clientcode
        WHERE judge = 'False'
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template("table.html",
                           title="濃厚接触者",
                           table_data=recset
                           )
