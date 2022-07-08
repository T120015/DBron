from crypt import methods
from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, session
from MyDatabase import my_open, my_query, my_close
import pandas as pd
from datetime import datetime

# Constructor
app = Flask(__name__, static_folder="static")
#暗号化キー
app.secret_key = 'room11pass1234'
#timeOut
app.permanent_session_lifetime = timedelta(minutes=5)


dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'testdb'  # オープンするデータベース名
}

# ログイン処理
@app.route('/login/<string:msg>', methods=["get"])
def login(msg):
    return render_template(
        "login.html",
        title="健康記録ログイン"
    )


@app.route("/login1", methods=['post'])
def login1():
    
    code = request.form['clientcode']
    password = request.form['pass']

    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from client
        where clientcode = '{code}'
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    my_close(dbcon, cur)
    print(recset)

    if password == recset['pass'][0]:
        session.permanent = True
        session["id"] = code
        return redirect(url_for('top'))
    else:
        return redirect(url_for('login', msg="IDかPassWordが違います．"))

# トップページ


@app.route("/")

def top():
    if "id" in session:
        return redirect(url_for('login'))

    title = "メインメニュー"
    
    return render_template(
        "top.html",
        title=title,
        msg="main src"
    )

        


@app.route("/table")

def table():
    if "id" in session:
        return redirect()
    dbcon, cur = my_open(**dsn)
    sql = f"""
        select * 
        from reportdb
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    return render_template(
        "table.html",
        title=f"",
        table_data=recset
    )

#健康記録
@app.route("/kenkou")
def kenkou():
    return render_template(
        "form_kenkou.html",
        title = "健康記録"
    )

@app.route("kenkou1",methods=["POST"])
def kenkou1():
    
    clientcode = request.form["clientcode"]
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

    dbcon,cur = my_open( **dsn )
    
    sqlstring = f"""
        INSERT INTO kansatu
        (clientcode,record,meridiem,temp,pain,feeling,headache,
        throat,breathness,cough,nausea,diarrhea,
        taste,olfactory,lastupdate)
        VALUES
        ('{clientcode}','{record}','{meridiem}','{temp}','{pain}','{feeling}','{headache}',
        '{throat}','{breathness}','{cough}','{nausea}','{diarrhea}',
        '{taste}','{olfactory}','{dt_now}')
        ;
    """
    my_query(sqlstring,cur)
    dbcon.commit()

    return render_template(
        "msg.html",
        title = "健康記録",
        message = "健康記録を保存しました"
    )

@app.route("/koudou")
def koudou():
    return render_template(
        "form_koudou.html",
        title = "行動記録"
    )

@app.route("/koudou1", methods = ['POST'])
def koudou1():

    import datetime
    dt_now = datetime.datetime.now()
    
    action = request.form['action']
    start = request.form['start']
    end = request.form['end']
    location = request.form['location']
    move = request.form['move']
    departure = request.form['departure']
    arrival = request.form['arrival']
    companions = request.form['companions']
    clientcode = session["id"]

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        INSERT INTO koudou
        (clientcode, action, start, end, location, move, departure, arrival, companions, lastupdate)
        values
        ('{clientcode}', '{action}', '{start}', '{end}', '{location}', '{move}', '{departure}', '{arrival}', '{companions}', '{dt_now}')
    """

    my_query(sqlstring, cur)
    
    dbcon.commit()
    if companions == 1:
        return redirect(url_for('shosai'))
    else:   
        return render_template(
            "msg.html",
            title = "行動記録完了",
            message = "行動記録を保存しました。"
        )

@app.route("/shosai", methods = ['POST'])
def koudou2():

    import datetime
    dt_now = datetime.datetime.now()
    
    who = request.form['action']
    people_num = request.form['start']
    num = request.form['num']
    remarks = request.form['end']
    clientcode = session["id"]

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        select *
        from koudou
        where clientcode = '{clientcode}'
        ;
    """ 

    my_query(sqlstring, cur)    
    recset = pd.DataFrame(cur.fetchall())
    koudouID = pd.max(recset[koudouID])

    sqlstring = f"""
        INSERT INTO koudou_shosai
        (koudouID, who, people_num, remarks, lastupdate)
        values
        ({koudouID}, '{who}', {people_num}, '{remarks}', '{dt_now}')
    """

    my_query(sqlstring, cur)
    
    dbcon.commit()
    if num >= 1:
        return redirect(url_for('shosai1'))
    else:   
        return render_template(
            "msg.html",
            title = "行動記録完了",
            message = "行動記録を保存しました。"
        )

@app.route("/shosai1", methods = ['POST'])
def koudou2():

    import datetime
    dt_now = datetime.datetime.now()
    
    who = request.form['action']
    people_num = request.form['start']
    num = request.form['num']
    remarks = request.form['end']
    clientcode = session["id"]

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        select *
        from koudou
        where clientcode = '{clientcode}'
        ;
    """ 

    my_query(sqlstring, cur)    
    recset = pd.DataFrame(cur.fetchall())
    koudouID = pd.max(recset[koudouID])

    sqlstring = f"""
        INSERT INTO koudou_shosai
        (koudouID, who, people_num, remarks, lastupdate)
        values
        ({koudouID}, '{who}', {people_num}, '{remarks}', '{dt_now}')
    """

    my_query(sqlstring, cur)
    
    dbcon.commit()
    if num >= 1:
        return redirect(url_for('shosai1'))
    else:   
        return render_template(
            "msg.html",
            title = "行動記録完了",
            message = "行動記録を保存しました。"
        )

# 管理者系


@app.route("/manage")
def manage():
    return render_template(
        "manage.html",
        title="管理者メニュー"
    )


@app.route("/manage/insert")
def insert():
    return render_template(
        "insert.html",
        title="関係者追加"
    )

#コロナ記録
@app.route("corona")
def corona():
    return render_template(
        "form_corona.html",
        title="コロナ陽性・濃厚接触者記録"
    )

@app.route("corona1")
def corona1():
    clientcode = request.form["clientcode"]
    judge = request.form["judge"]
    onset = request.form["onset"]
    stopflag = request.form["stopflag"]

    import datetime
    dt_now = datetime.datetime.now

    dbcon,cur = my_open( **dsn ) 

    sqlstring = f"""
        INSERT INTO corona
        (clientcode,judge,onset,stopflag,lastupdate)
        VALUES
        ('{clientcode}','{judge}','{onset}','{stopflag}','{dt_now}')
        ;
    """
    my_query(sqlstring,cur)
    dbcon.commit()
    my_close(dbcon,cur)

    return render_template(
        "msg.html",
        title = "コロナ陽性・濃厚接触者記録",
        message = "記録しました"
    )
    


# サーバ起動
app.run('127.0.0.1', 5000, True)
