from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, url_for, redirect, session
from MyDatabase import my_open, my_query, my_close
import pandas as pd
from datetime import datetime, date, timedelta
from Manager import mng
from Client import cnt
from Koudou import kdu
from Kansatsu import rec
from smtplib import SMTP
from email.mime.text import MIMEText

dsn = {
    "host": "172.30.0.10",  # ホスト名(IPアドレス)
    "port": "3306",  # mysqlの接続ポート番号
    "user": "root",  # dbアクセスするためのユーザid
    "password": "1234",  # ユーザidに対応するパスワード
    "database": "dbron",  # オープンするデータベース名
}


# Constructor
app = Flask(__name__, static_folder="static")
# 暗号化キー
app.secret_key = "room11pass1234"


# from Other_method
app.register_blueprint(mng)
app.register_blueprint(cnt)
app.register_blueprint(kdu)
app.register_blueprint(rec)


def send_email(to_BCC):

    # 送受信先
    from_email = "zen.aku_movie@outlook.com"

    # MIMETextを作成
    body = "昨日の記録が未登録です.\n早急に健康記録を登録してください."
    msg = MIMEText(body, "html")
    msg["Subject"] = "昨日の健康記録が未登録です"
    msg["From"] = from_email
    msg["Bcc"] = ";".join(to_BCC)

    # サーバを指定する
    server = SMTP("smtp.office365.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # メールを送信する
    server.login(from_email, "ZenAkuMovie5963")
    server.send_message(msg)
    # debug for email
    # server.set_debuglevel(True)
    # 閉じる
    server.quit()


def check_contact():
    # 濃厚接触者のストップフラグを解除
    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from corona
        where judge = 0
        and stopflag = 1
        and delflag = False
        ;
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())
    debug = timedelta(days=7)

    for ind, item in recset.iterrows():
        if(date.today() - item['onset']) >= debug:
            sql = f"""
                update corona
                set stopflag = 0
                where onset = '{item['onset']}'
                and clientcode = '{item['clientcode']}'
                ;
            """
            my_query(sql, cur)
            dbcon.commit()

    my_close(dbcon, cur)


def check_record():
    # 記録がない人に自動でメール
    yesterday = date.today() - timedelta(days=1)

    dbcon, cur = my_open(**dsn)

    sql = f"""
        select *
        from client
        where delflag = 0
        ;
    """
    my_query(sql, cur)
    clients = pd.DataFrame(cur.fetchall())
    no_list = []
    # レコードの有無を判定
    for _, client in clients.iterrows():
        sql = f"""
            select *
            from kansatu
            where clientcode = '{client['clientcode']}'
            and record = '{yesterday}'
            and delflag = 0
            ;
        """
        my_query(sql, cur)
        recset = pd.DataFrame(cur.fetchall())
        if recset.empty:
            no_list.append(client['email'])

        if no_list != None:
            send_email(no_list)


def check_tables():
    # 毎日4:00実行する
    check_contact()
    check_record()


@app.before_first_request
def schedule():
    task = BackgroundScheduler(daemon=True)
    # タスクの実行時間と実行処理
    # for debug
    task.add_job(check_tables, 'interval', minutes=1)

    #task.add_job(check_tables, 'cron', hour=4)
    task.start()


@app.before_request
def checkSession():
    # session に記録があるか判定
    if request.endpoint not in ('login', 'login1', 'logout', 'static'):
        if not "id" in session:
            return redirect(url_for("login"))
        elif session['school'] < 7:
            app.permanent_session_lifetime = timedelta(minutes=5)
        else:
            app.permanent_session_lifetime = timedelta(days=1)


@app.route("/login")
@app.route("/login/<string:msg>")
def login(msg=""):
    # ログイン
    return render_template("login.html", title="健康記録ログイン", msg=msg)


@app.route("/login1", methods=["post"])
def login1():
    clientcode = request.form["clientcode"].upper()
    password = request.form["pass"]
    # for debug
    # print(clientcode, password)

    dbcon, cur = my_open(**dsn)
    # DBにレコードがあるか確認
    sql = f"""
        select *
        from client
        where clientcode = '{clientcode}'
    """
    my_query(sql, cur)
    recset = pd.DataFrame(cur.fetchall())

    my_close(dbcon, cur)
    if recset.empty:
        # レコードがなければはじく
        return redirect(url_for("login", msg="IDかPassWordが違います."))
    elif password != recset["pass"][0]:
        # PASSが違えばはじく
        return redirect(url_for("login", msg="IDかPassWordが違います."))
    else:
        # セッションに記録
        session["id"] = clientcode
        session["school"] = recset["schoolID"][0].astype("object")
        print(session)
        return redirect(url_for("cnt.top"))


@app.route("/logout")
def logout():
    # ログアウト処理
    session.pop("id", None)
    session.pop("school", None)
    session.clear()
    print(session)
    return redirect(url_for("login"))


# サーバ起動
app.run("127.0.0.1", 5000, debug=True)
