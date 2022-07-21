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
    'database': 'dbron'  # オープンするデータベース名
}

@rec.route("/kenkou")
def kenkou():
    return render_template(
        "form_kenkou.html",
        title="健康記録",
        today = date.today(),
        to_url = "/kenkou1"
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

    dt_now = datetime.now()

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        INSERT INTO kansatu
        (clientcode,record,meridiem,temp,pain,feeling,headache,
        throat,breathness,cough,nausea,diarrhea,
        taste,olfactory,lastupdate)
        VALUES
        ('{code}','{record}','{meridiem}',{temp},{pain},{feeling},{headache},
        {throat},{breathness},{cough},{nausea},{diarrhea},
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


@rec.route("/update_kansatu")
def update_kansatu():
    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select *
        from kansatu
        where delflag = False
        and clientcode = '{session['id']}'
        ;
    """

    #クエリを実行
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    recset = recset.loc[:, :'lastupdate']

    #データベースをクローズ
    my_close(dbcon, cur)

    li = ['編集ボタン', '削除ボタン', '記録日', 'AM/PM', '体温', '関節・筋肉痛', 'だるさ', '頭痛',
          '咽頭痛', '息苦しさ', '咳・くしゃみ', '吐気・嘔吐', '腹痛・下痢', '味覚障害', '嗅覚障害', '最終更新日']

    return render_template(
        "table_update.html",
        title="キャンセルレコード選択画面",
        table_data=recset,
        list=li,
        name='kansatuID',
        action_edit='/update1_kansatu',
        action_delete='/delete_kansatu'
    )


@rec.route("/update1_kansatu", methods=['POST'])
def update1_kansatu():
    kansatuID = request.form['kansatuID']
    session['kansatuID'] = kansatuID

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        select *
        from kansatu
        where kansatuID = {kansatuID}
        ;
    """
    my_query(sqlstring, cur)

    recset = pd.DataFrame(cur.fetchall())

    my_close(dbcon, cur)

    return render_template(
        "form_kenkou.html",
        title="健康記録更新",
        url_for='/update2_kansatu',
        record=recset['record'][0],
        meridiem=recset['meridiem'][0],
        temp=recset['temp'][0],
        pain=recset['pain'][0],
        feeling=recset['feeling'][0],
        headache=recset['headache'][0],
        throat=recset['throat'][0],
        breathness=recset['breathness'][0],
        cough=recset['cough'][0],
        nausea=recset['nausea'][0],
        diarrhea=recset['diarrhea'][0],
        taste=recset['taste'][0],
        olfactory=recset['olfactory'][0]
    )


@rec.route("/update2_kansatu", methods=['POST'])
def update2_kansatu():
    clientcode = session["id"]
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
    kansatuID = session['kansatuID']
    dt_now = datetime.now()

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        update kansatu
        set
        clientcode = '{clientcode}',
        record = '{record}',
        temp = {temp},
        meridiem = '{meridiem}',
        pain = {pain},
        feeling = {feeling},
        headache = {headache},
        throat = {throat},
        breathness = {breathness},
        cough = {cough},
        nausea = {nausea},
        diarrhea = {diarrhea},
        taste = {taste},
        olfactory = {olfactory},
        lastupdate = '{dt_now}'
        where kansatuID = {kansatuID}
        ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "msg.html",
        title="健康記録更新",
        message="健康記録を更新しました"
    )


@rec.route("/delete_kansatu", methods=['POST'])
def delete_kansatu():
    #データベースをオープン
    dbcon, cur = my_open(**dsn)

    #現在時刻を取得
    dt_now = datetime.now()

    #form変数を受取
    kansatuID = request.form['kansatuID']

    sqlstring = f"""
        update kansatu
        set
        lastupdate = '{dt_now}',
        delflag = True
        where kansatuID = {kansatuID}
        ;
    """
    my_query(sqlstring, cur)

    #テーブルに変更を適用
    dbcon.commit()
    #データベースをクローズ
    my_close(dbcon, cur)
    #実行終了
    return render_template(
        "msg.html",
        title="健康記録削除",
        message="健康記録を削除しました。"
    )
