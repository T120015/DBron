from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, session
from MyDatabase import my_open, my_query, my_close
import pandas as pd
from datetime import datetime
from Manager import mng
from Client import cnt
from Koudou import kdu
from Kansatsu import rec

# Constructor
app = Flask(__name__, static_folder="static")
# 暗号化キー
app.secret_key = "room11pass1234"

# from manager_method
app.register_blueprint(mng)
app.register_blueprint(cnt)
app.register_blueprint(kdu)
app.register_blueprint(rec)

@app.before_request
def checkSession():
    if request.endpoint not in ('login', 'login1', 'logout', 'static'):
        if not "id" in session:
            return redirect(url_for("login"))
        elif session['school'] < 7:
            app.permanent_session_lifetime = timedelta(minutes=5)
        else:
            app.permanent_session_lifetime = timedelta(days=5)


dsn = {
    "host": "172.30.0.10",  # ホスト名(IPアドレス)
    "port": "3306",  # mysqlの接続ポート番号
    "user": "root",  # dbアクセスするためのユーザid
    "password": "1234",  # ユーザidに対応するパスワード
    "database": "dbron",  # オープンするデータベース名
}


@app.route("/login")
@app.route("/login/<string:msg>")
def login(msg=""):
    # ログイン処理
    return render_template("login.html", title="健康記録ログイン", msg=msg)


@app.route("/login1", methods=["post"])
def login1():
    clientcode = request.form["clientcode"]
    password = request.form["pass"]
    # for debug
    # print(clientcode, password)

    

    dbcon, cur = my_open(**dsn)
    
    sql = f"""
        select *
        from client
        where clientcode = '{clientcode.upper()}'
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    my_close(dbcon, cur)

    if recset.empty:
        return redirect(url_for("login", msg="IDかPassWordが違います."))
    elif password != recset["pass"][0]:
        return redirect(url_for("login", msg="IDかPassWordが違います."))
    else:
        session["id"] = clientcode
        session["school"] = recset["schoolID"][0].astype("object")
        if session["school"] >= 7:
            session.permanent = True
        print(session)
        return redirect(url_for("cnt.top"))


@app.route("/logout")
def logout():
    # ログアウト処理
    session.pop("id", None)
    session.pop("school", None)
    session.clear()
    return redirect(url_for("login"))

@app.route("/corona")
def corona():
    # コロナ記録
    return render_template("form_corona.html", title="コロナ陽性・濃厚接触者記録")


@app.route("/corona1")
def corona1():
    clientcode = request.form["clientcode"]
    judge = request.form["judge"]
    onset = request.form["onset"]
    stopflag = request.form["stopflag"]

    dt_now = datetime.now()

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        INSERT INTO corona
        (clientcode,judge,onset,stopflag,lastupdate)
        VALUES
        ('{clientcode}','{judge}','{onset}','{stopflag}','{dt_now}')
        ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template("msg.html", title="コロナ陽性・濃厚接触者記録", message="記録しました")


# サーバ起動
app.run("127.0.0.1", 5000, True)
