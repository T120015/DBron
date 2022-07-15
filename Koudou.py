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

kdu = Blueprint('kdu', __name__)


@kdu.route("/koudou")
def koudou():
    #行動記録
    return render_template(
        "form_koudou.html",
        title="行動記録"
    )


@kdu.route("/koudou1", methods=['POST'])
def koudou1():

    #現在時刻の取得
    dt_now = datetime.now()

    #form変数の受取
    action = request.form['action']
    start = request.form['start']
    end = request.form['end']
    location = request.form['location']
    move = request.form['move']
    departure = request.form['departure']
    arrival = request.form['arrival']
    companions = request.form['companions']
    #sessionからclientcodeの受取
    clientcode = session["id"]

    #データベースオープン
    dbcon, cur = my_open(**dsn)

    #koudouテーブルにデータを挿入
    sqlstring = f"""
        INSERT INTO koudou
        (clientcode, action, start, end, location, move, departure, arrival, companions, lastupdate)
        values
        ('{clientcode}', '{action}', '{start}', '{end}', '{location}', '{move}', '{departure}', '{arrival}', '{companions}', '{dt_now}')
    """
    #sqlを実行
    my_query(sqlstring, cur)

    #変更を適用
    dbcon.commit()
    #データベースをクローズ
    my_close(dbcon, cur)

    #同行者がTrueの時、form_shosaiに移動
    if int(companions) == 1:
        return render_template(
            "form_shosai.html",
            title="行動詳細記録ページ"
        )
    #同行者がFalseの時、入力を終了
    else:
        return render_template(
            "msg.html",
            title="行動記録完了",
            message="行動記録を保存しました。"
        )


@kdu.route("/shosai", methods=['POST'])
def shosai():
    #現在時刻を取得
    dt_now = datetime.now()

    #form変数を受取
    who = request.form['who']
    people_num = request.form['people_num']
    num = int(request.form['num'])
    remarks = request.form['remarks']
    #sessionからclientcodeを受取
    clientcode = session["id"]

    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select *
        from koudou
        where clientcode = '{clientcode}'
        ;
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #引き出したテーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    #最新のkoudouIDをkoudouIDに格納
    koudouID = recset['koudouID'].max()

    #koudou_shosaiテーブルにデータを挿入
    sqlstring = f"""
        INSERT INTO koudou_shosai
        (koudouID, who, people_num, remarks, lastupdate)
        values
        ({koudouID}, '{who}', {people_num}, '{remarks}', '{dt_now}')
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #テーブルに変更を適用
    dbcon.commit()
    #データベースをクローズ
    my_close(dbcon, cur)

    #同大学の同行者が1人以上の時、form_friendに移動
    if num >= 1:
        return render_template(
            "form_friend.html",
            title="同行者記録ページ",
            msg="同行者を入力してください",
            num=num
        )
    #同大学の同行者がいない時、入力を終了
    else:
        return render_template(
            "msg.html",
            title="行動記録完了",
            message="行動記録を保存しました。"
        )


@kdu.route("/friend", methods=['POST'])
def shosai1():
    #データベースをオープン
    dbcon, cur = my_open(**dsn)

    #form変数を受取
    num = int(request.form['num'])
    #sessionからclientcodeを受取
    clientcode = session["id"]
    #同行者のclientcodeをflientcodeにlist型として格納
    friendcode = []
    for i in range(num):
        friendcode.append(request.form[f'friendcode{i + 1}'])

    #clienttableからデータを受取
    sqlstring = f"""
        select *
        from client
        ;
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    #受け取ったcientcodeに誤りがないかの判定
    for item in friendcode:
        #flagをリセット
        flag = 0
        for ind, rowdata in recset.iterrows():
            if item == rowdata['clientcode']:
                #clientcodeが一致したらflagを立てる
                flag = 1
        #もしflagが立っていなかったとき、clientcodeに誤り有
        #form_friendで入力しなおし
        if flag == 0:
            return render_template(
                "form_friend.html",
                title="同行者記録ページ",
                msg="学籍番号に誤りがあります。正しい学籍番号を入力してください。",
                num=num
            )

    #koudouテーブルからclientcodeが等しいテーブルデータを受取
    sqlstring = f"""
        select *
        from koudou
        where clientcode = '{clientcode}'
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    #最新のkoudouIDをkoudouIDに格納
    koudouID = recset['koudouID'].max()

    #koudou_shosaiテーブルからkoudouIDが等しいテーブルデータを受取
    sqlstring = f"""
        select *
        from koudou_shosai
        where koudouID = {koudouID}
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    #最新のshosaiIDをshosaiIDに格納
    shosaiID = recset['shosaiID'].max()

    #koudou_friendテーブルにデータを挿入
    for item in friendcode:
        sqlstring = f"""
            INSERT INTO koudou_friend
            (shosaiID, friendcode)
            values
            ({shosaiID}, '{item}')
        """
        #クエリを実行
        my_query(sqlstring, cur)

    #テーブルに変更を適用
    dbcon.commit()
    #データベースをクローズ
    my_close(dbcon, cur)

    #実行終了
    return render_template(
        "msg.html",
        title="行動記録完了",
        message="行動記録を保存しました。"
    )


@kdu.route("/update")
def update():

    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select *
        from koudou_all
        ;
    """

    #クエリを実行
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    recset = recset.loc['koudouID', 'action', 'start', 'end', 'location', 'move',
                        'departure', 'companions', 'who', 'people_num', 'remarks', 'friendcode', 'lastupdate']
    #データベースをクローズ
    my_close(dbcon, cur)

    return render_template(
        "table_update.html",
        title="キャンセルレコード選択画面",
        table_data=recset
    )


@kdu.route("/update1", methods=['POST'])
def update1():

    koudouID = request.form['koudouID']

    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select *
        from koudou
        where koudouID = '{koudouID}'
        ;
    """

    #クエリを実行
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    #データベースをクローズ
    my_close(dbcon, cur)

    return render_template(
        "table_update.html",
        title="キャンセルレコード選択画面",
        table_data=recset
    )
