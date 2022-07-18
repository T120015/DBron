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
    #管理者権限の有無
    if session["school"] < 7:
        return render_template(
            "msg.html",
            title="アクセスできません",
            msg="このアカウントは管理者権限がありません."
        )


@mng.route("/", methods=['get', 'post'])
def manage():
    # 管理者メニュー
    return render_template(
        "manage.html",
        title="管理者メニュー"
    )


@mng.route("/table")
def table():
    # 一覧表示
    dbcon, cur = my_open(**dsn)
    sql = f"""
        select *
        from acount
        where delflag = 0
        ;
    """
    column_list = ['CODE', '区分', '部類', 'PASSWORD', '氏名',
                   '年齢', '性別', '電話番号', 'メール', '所属部所', '最終更新日']
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "manage_list.html",
        title="関係者一覧",
        column_list=column_list,
        table_data=recset.loc[:, 'clientcode':'lastupdate'].sort_values(
            'clientcode')
    )


@mng.route("/insert")
def insert():
    # 関係者追加
    dbcon, cur = my_open(**dsn)
    
    #区分，部類を取得
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
        "manage_input.html",
        title="関係者追加",
        input_position=position,
        input_class=cls,
        url="/",
        to_url="/insert1",
        position="",
        cls=""
    )


@mng.route("/insert1", methods=['post'])
def insert1():
    position = request.form['position']
    cls = request.form['class']
    code = request.form['clientcode']
    password = request.form['pass']
    namae = request.form['namae']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    email = request.form['email']
    faculty = request.form['faculty']

    dbcon, cur = my_open(**dsn)
    #区分，部類を取得
    sql = f"""
        select *
        from school
        where position = '{position}'
        and class = '{cls}'
    """
    my_query(sql, cur)
    df = pd.DataFrame(cur.fetchall())
    #レコードを追加
    sql = f"""
        insert into client
        (schoolID, clientcode, pass, namae, age, gender, phone, email, faculty)
        value
        ({df['schoolID'][0]}, '{code}', '{password}', '{namae}', {age}, '{gender}', '{phone}', '{email}','{faculty}')
    """
    my_query(sql, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "manage_msg.html",
        title="関係者追加完了",
        message=f"{code}:{namae}を追加しました．"
    )


@mng.route("/insert_files")
def insert_files():
    # ファイル読み込み
    return render_template(
        "manage_files.html",
        title="関係者追加"
    )


@mng.route("/upload_csv", methods=['post'])
def upload_csv():
    # csvFileの受け取り
    csv_file = request.files['upfile']
    msg = csv2df(csv_file)

    return render_template(
        "manage_msg.html",
        title="追加完了",
        message=msg
    )


@mng.route("/select")
def select():
    # 関係者編集
    return render_template(
        "manage_select.html",
        title="関係者情報"
    )


@mng.route("/select1", methods=['post'])
def select1():
    code = request.form['clientcode'].upper()
    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from acount
        where clientcode = '{code}'
        and delflag = 0
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    print(recset["namae"])
    return render_template(
        "manage_show.html",
        title=f"{code}の情報",
        name=recset["namae"][0],
        gender=recset["gender"][0],
        age=recset["age"][0],
        pswd = recset["pass"][0],
        phone=recset["phone"][0],
        email=recset["email"][0],
        faculty=recset["faculty"][0],
        position=recset["position"][0],
        cls=recset["class"][0],
        code=code,
        url="/delete"
    )


@mng.route("/update", methods=['post'])
def update():
    # レコード編集
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
        and delflag = 0
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    return render_template(
        "manage_input.html",
        title=f"{code}の編集",
        input_position=position,
        input_class=cls,
        url="/select1",
        name=recset["namae"][0],
        gender=recset["gender"][0],
        age=recset["age"][0],
        pswd=recset["pass"][0],
        phone=recset["phone"][0],
        email=recset["email"][0],
        faculty=recset["faculty"][0],
        position=recset["position"][0],
        cls=recset["class"][0],
        code=code
    )


@mng.route("/delete", methods=['post'])
def delete():
    #レコード削除
    code = request.form['clientcode']
    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from acount
        where clientcode = '{code}'
        and delflag = 0
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    return render_template(
        "manage_show.html",
        title=f"{code}の削除",
        name=recset["namae"][0],
        gender=recset["gender"][0],
        age=recset["age"][0],
        phone=recset["phone"][0],
        email=recset["email"][0],
        faculty=recset["faculty"][0],
        position=recset["position"][0],
        cls=recset["class"][0],
        code=code,
        url="/delete1"
    )


@mng.route("/delete1", methods=['post'])
def delete1():
    code = request.form['clientcode']

    dbcon, cur = my_open(**dsn)
    sql = f"""
        update client
        set
        delflag = 1        
        where clientcode = '{code}'
        ;
    """
    my_query(sql, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "manage_msg.html",
        title=f"{code}削除完了",
        message=f"削除が完了しました．"
    )


@mng.route("/no_record")
def no_record():
    #3日以上連続して記録がない
    dbcon, cur = my_open(**dsn)

    sql = f"""
        SELECT *
        FROM kansatu
        right outer JOIN client
        on kansatu.clientcode = client.clientcode
        ;
    """
    my_query(sql, cur)
    #レコードを取得
    recset = pd.DataFrame(cur.fetchall())
    li = list()
    delta = timedelta(days=3)

    for item in recset.values:
        #3日以上かどうか
        if item[2] == None:
            #記録なし
            li.append([item[1], item[20]])
        else:
            #記録あり
            debug = date.today() - item[2]
            if debug > delta:
                li.append(item[1])

    li = pd.DataFrame(li, columns=['clientcode'])
    #print(li)

    my_close(dbcon, cur)

    return render_template(
        "manage_table.html",
        title="3日以上連続記録なし",
        table_data=li
    )


@mng.route("/health")
def health():
    today = date.today()
    week = []
    for day in range(7,-1,-1):
        week.append(today-timedelta(days=day))
    dbcon, cur = my_open(**dsn)
    column_list = ["CODE", "氏名"]
    table=[]
    for day in week:
        #print(day)
        sql = f"""
            SELECT *
            FROM kansatu
            left outer JOIN client
            on kansatu.clientcode = client.clientcode
            where record = '{day}'
            ;
        """
        my_query(sql, cur)
        recset = pd.DataFrame(cur.fetchall())

        li = list()
        for item in recset.values:
            flag = 0
            for ck in item:
                if ck == 1 or ck == 0:
                    flag += ck
            if (item[4] >= 37.5) or (flag >= 5):
                sql =f"""
                    select *
                    from client
                    where clientcode = '{item[1]}'
                    ;
                """
                my_query(sql, cur)
                df = pd.DataFrame(cur.fetchall())
                li.append([item[1], df['namae'][0]])

        li = pd.DataFrame(li, columns=column_list)
        table.append(li)

    my_close(dbcon, cur)
    return render_template(
        "manage_table.html",
        title="37.5度以上or5個チェックの人",
        week = week,
        column_list=column_list,
        table_data=table
    )


@mng.route("/corona")
def corona():
    column_list = ['CODE', '氏名', '診断病院', '診断日', 'ストップフラグ']
    dbcon, cur = my_open(**dsn)

    sql = f"""
        SELECT *
        FROM corona
        inner join client
        on corona.clientcode = client.clientcode
        WHERE judge = True
        AND corona.delflag = False
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "manage_list.html",
        title="コロナ感染者",
        column_list = column_list,
        table_data=recset
    )


@mng.route("/close_contact")
def close_contact():

    dbcon, cur = my_open(**dsn)

    sql = f"""
        SELECT *
        FROM corona
        WHERE judge = False
        AND delflag = False
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "manage_list.html",
        title="濃厚接触者",
        table_data=recset
    )
