from crypt import methods
from turtle import position
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
    # 管理者権限の有無
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
    # カラムリスト
    column_list = ['CODE', '区分', '部類', 'PASSWORD', '氏名',
                   '年齢', '性別', '電話番号', 'メール', '所属部所', '最終更新日']
    # クエリ実行
    my_query(sql, cur)
    # DataFlameに格納
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

    # 区分，部類を取得
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
    # 区分，部類を取得
    sql = f"""
        select *
        from school
        where position = '{position}'
        and class = '{cls}'
    """
    my_query(sql, cur)
    df = pd.DataFrame(cur.fetchall())
    # レコードを追加
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
        title="関係者情報",
        to_url="/select1"
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
    print(recset.empty)
    if recset.empty:
        return render_template(
            "manage_select.html",
            title="関係者情報",
            msg=f"関係者コード:{code}は存在しません．"
        )
    else:
        return render_template(
            "manage_show.html",
            title=f"{code}の情報",
            name=recset["namae"][0],
            gender=recset["gender"][0],
            age=recset["age"][0],
            pswd=recset["pass"][0],
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
        to_url = "/update1",
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

@mng.route("/update1", methods=['post'])
def update1():
    old_code = request.form["old_code"]
    code = request.form["clientcode"]
    position = request.form["position"]
    cls = request.form["class"]
    pswd = request.form["pass"]
    namae = request.form["namae"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    email = request.form["email"]
    faculty = request.form["faculty"]
    
    dbcon, cur = my_open(**dsn)
    
    sql = f"""
        select schoolID
        from school
        where position = '{position}'
        and class = '{cls}'
        and delflag = 0
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    school = recset["schoolID"][0]
    sql = f"""
        update client
        set
        schoolID = {school},
        clientcode = '{code}',

        pass = '{pswd}',
        namae = '{namae}',
        age = {age},
        gender = '{gender}',
        phone = '{phone}',
        email = '{email}',     
        faculty = '{faculty}',
        lastupdate = '{datetime.now()}'
        where clientcode = '{old_code}'
        and delflag = 0
        ;
    """
    my_query(sql, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "manage_msg.html",
        title = f"{code}編集完了",
        message = f"編集が完了しました."
    )

@mng.route("/delete", methods=['post'])
def delete():
    # レコード削除
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
        delflag = 1,
        lastupdate = '{datetime.now()}'
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


@mng.route("/show_record")
def show_record():
    # 関係者編集
    return render_template(
        "manage_select.html",
        title="関係者記録情報",
        to_url = "/show_record1"
    )


@mng.route("/show_record1", methods=['post'])
def show_record1():
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
    print(recset.empty)
    if recset.empty:
        return render_template(
            "manage_select.html",
            title="関係者情報",
            msg=f"関係者コード:{code}は存在しません．"
        )
    else:
        return render_template(
            "manage_record.html",
            title=f"{code}の記録情報",
            code=code
        )

@mng.route("/show_record2", methods=['post'])
def show_record2():
    code = request.form["clientcode"]
    to_url = request.form["url"]

    return redirect(url_for(f"mng.{to_url}", code=code))


@mng.route("/show_koudou/<string:code>")
def show_koudou(code):

    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select distinct koudouID, shosaiID, action, start, end, location, move, departure, arrival, companions, who, people_num, remarks, lastupdate
        from koudou_all
        where clientcode = '{code}'
        and delflag = False
        ;
    """

    #クエリを実行
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    recset = recset.loc[:, :'lastupdate']

    print(recset)

    sqlstring = f"""
        select shosaiID, friendcode
        from koudou_friend
        where delflag = False
        ;
    """
    #クエリを実行
    my_query(sqlstring, cur)

    ls = pd.DataFrame(cur.fetchall())
    df = pd.DataFrame(index=[], columns=['shosaiID', 'friendcode'])
    #データベースをクローズ
    my_close(dbcon, cur)

    for i in recset.values:
        li = list()
        for j in ls.values:
            if i[1] == j[0]:
                li.append(j[1])
        df = df.append({'shosaiID': i[1], 'friendcode': li}, ignore_index=True)

    recset.insert(12, 'friendcode', df['friendcode'])

    df = pd.DataFrame(index=[], columns=['start', 'end'])

    for ind, rowdata in recset.iterrows():
        sec_s = rowdata[3].total_seconds()
        sec_e = rowdata[4].total_seconds()
        hour_s = int(sec_s/3600)
        hour_e = int(sec_e/3600)
        min_s = int((sec_s/3600 - hour_s)*60)
        min_e = int((sec_e/3600 - hour_e)*60)
        df = df.append({'start': f'{str(hour_s).zfill(2)}:{str(min_s).zfill(2)}',
                       'end': f'{str(hour_e).zfill(2)}:{str(min_e).zfill(2)}'}, ignore_index=True)
    recset = recset.drop(columns=['start', 'end'])
    recset.insert(3, 'start', df['start'])
    recset.insert(4, 'end', df['end'])

    li = ['行動日', '開始時間', '終了時間', '行き先', '移動方法',
          '出発地', '目的地', '同行者', '同行者', '人数', '同行者学籍番号', '備考', '最終更新日']

    return render_template(
        "manage_table.html",
        title="キャンセルレコード選択画面",
        table_data=recset,
        list=li,
        name='koudouID',
        action_edit='/update1_koudou',
        action_delete='/delete_koudou'
    )


@mng.route("/no_record")
def no_record():
    # 3日以上連続して記録がない
    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from client
        where delflag = 0
        ;
    """
    my_query(sql, cur)
    clients = pd.DataFrame(cur.fetchall())

    li = []
    # 記録の判定
    delta = timedelta(days=3)
    for _, client in clients.iterrows():
        # SQL呼び出し
        sql = f"""
            select *
            from kansatu
            where clientcode = '{client["clientcode"]}'
            and delflag = 0
            ;
        """
        my_query(sql, cur)
        # レコードを取得
        recset = pd.DataFrame(cur.fetchall())

        if not recset.empty:
            if (date.today() - recset["record"].max()) < delta:
                continue
        #print(client.loc[["clientcode", "namae", "phone", "email"]])
        li.append([client["clientcode"],client["namae"], client["phone"], client["email"]])

    column_list = ["CODE", "氏名", "電話番号", "Email"]
    table = pd.DataFrame(li, columns=column_list)
    print(table)

    my_close(dbcon, cur)

    return render_template(
        "manage_list.html",
        title="3日以上連続記録なし",
        column_list=column_list,
        table_data=table
    )


@mng.route("/health")
def health():
    today = date.today()
    week = []
    for day in range(7, -1, -1):
        week.append(today-timedelta(days=day))
    dbcon, cur = my_open(**dsn)
    column_list = ["CODE", "氏名"]
    table = []
    for day in week:
        # print(day)
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
                sql = f"""
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
        week=week,
        column_list=column_list,
        table_data=table
    )


@mng.route("/corona")
def corona():
    column_list = ['CODE', '氏名', '診断病院', '診断日', 'ストップフラグ']
    dbcon, cur = my_open(**dsn)

    sql = f"""
        SELECT client.clientcode, client.namae, hospital, onset,stopflag
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
        column_list=column_list,
        table_data=recset
    )


@mng.route("/close_contact")
def close_contact():

    dbcon, cur = my_open(**dsn)

    column_list = ['CODE', '氏名', '診断日', 'ストップフラグ']
    sql = f"""
        SELECT client.clientcode, client.namae, onset,stopflag
        FROM corona
        inner join client
        on corona.clientcode = client.clientcode
        WHERE judge = False
        AND corona.delflag = False
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "manage_list.html",
        title="濃厚接触者",
        column_list=column_list,
        table_data=recset
    )
