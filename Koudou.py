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
    dt_now = datetime.now()
    #行動記録
    return render_template(
        "form_koudou.html",
        to_url='/koudou1',
        title="行動記録",
        action=dt_now,
        start='00:00',
        end='00:00'
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
            to_url='/shosai',
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
    num = request.form['num']
    remarks = request.form['remarks']
    #sessionからclientcodeを受取
    clientcode = session["id"]

    if num == '':
        num = 0
    else:
        num = int(num)

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
            to_url='/friend',
            title="同行者記録ページ",
            msg="同行者を入力してください",
            num=num,
            friendcode=None
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

    #現在時刻を取得
    dt_now = datetime.now()
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
            if clientcode == rowdata['clientcode']:
                continue
            elif item == rowdata['clientcode']:
                #clientcodeが一致したらflagを立てる
                flag = 1
        #もしflagが立っていなかったとき、clientcodeに誤り有
        #form_friendで入力しなおし
        if flag == 0:
            return render_template(
                "form_friend.html",
                title="同行者記録ページ",
                msg="学籍番号に誤りがあります。正しい学籍番号を入力してください。",
                num=num,
                friendcode=None
            )

    #koudouテーブルからclientcodeが等しいテーブルデータを受取
    sqlstring = f"""
        select *
        from koudou
        where clientcode = '{clientcode}'
        ;
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
        and delflag = False
        ;
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
            (shosaiID, friendcode, lastupdate)
            values
            ({shosaiID}, '{item}', '{dt_now}')
            ;
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


@kdu.route("/update_koudou")
def update_koudou():

    #データベースをオープン
    dbcon, cur = my_open(**dsn)
    #koudouテーブルからclientcodeが等しいテーブルデータを引き出す
    sqlstring = f"""
        select distinct koudouID, shosaiID, action, start, end, location, move, departure, arrival, companions, who, people_num, remarks, lastupdate
        from koudou_all
        where clientcode = '{session['id']}'
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

    li = ['編集ボタン', '削除ボタン', '行動日', '開始時間', '終了時間', '行き先', '移動方法',
          '出発地', '目的地', '同行者', '同行者', '人数', '同行者学籍番号', '備考', '最終更新日']

    return render_template(
        "table_update.html",
        title="キャンセルレコード選択画面",
        table_data=recset,
        list=li,
        name='koudouID',
        action_edit='/update1_koudou',
        action_delete='/delete_koudou'
    )


@kdu.route("/update1_koudou", methods=['POST'])
def update1_koudou():

    koudouID = request.form['koudouID']
    session['koudouID'] = koudouID

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

    return render_template(
        "form_koudou.html",
        to_url='/update2_koudou',
        title="行動記録編集",
        action=recset['action'][0],
        start=recset['start'][0],
        end=recset['end'][0],
        location=recset['location'][0],
        move=recset['move'][0],
        departure=recset['departure'][0],
        arrival=recset['arrival'][0],
        companions=recset['companions'][0]
    )


@kdu.route("/update2_koudou", methods=['POST'])
def update2_koudou():
    koudouID = session['koudouID']
    action = request.form['action']
    start = request.form['start']
    end = request.form['end']
    location = request.form['location']
    move = request.form['move']
    departure = request.form['departure']
    companions = request.form['companions']
    dt_now = datetime.now()

    #dbオープン
    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        update koudou
        set
        action = '{action}',
        start = '{start}',
        end = '{end}',
        location = '{location}',
        move = '{move}',
        departure = '{departure}',
        companions = '{companions}',
        lastupdate = '{dt_now}'
        where koudouID = {koudouID}
        ;
    """

    #クエリを実行
    my_query(sqlstring, cur)

    dbcon.commit()

    sqlstring = f"""
        select *
        from koudou_shosai
        where koudouID = {koudouID}
        ;
    """
    #クエリを実行
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    if recset.empty:
        session.pop('koudouID', None)
        if companions == 1:
            return render_template(
                "form_shosai.html",
                to_url='/shosai',
                title="行動詳細記録ページ"
            )
        else:
            return render_template(
                "msg.html",
                title="行動記録編集完了",
                message="行動記録を編集しました。"
            )
    else:
        shosaiID = int(recset['shosaiID'][0])
        session['shosaiID'] = shosaiID

        sqlstring = f"""
            select *
            from koudou_friend
            where shosaiID = {shosaiID}
            and delflag = False
            ;
        """
        #クエリを実行
        my_query(sqlstring, cur)

        num = pd.DataFrame(cur.fetchall())
        if num.empty:
            num = 0
        else:
            num = len(num['friendcode'])

        session['num'] = num

        #データベースをクローズ
        my_close(dbcon, cur)

        #同行者がTrueの時、form_shosaiに移動
        if int(companions) == 1:
            return render_template(
                "form_shosai.html",
                to_url='/update3_koudou',
                title="行動詳細編集",
                who=recset['who'][0],
                people_num=recset['people_num'][0],
                num=num,
                remarks=recset['remarks'][0]
            )
        #同行者がFalseの時、入力を終了
        else:
            session.pop('num', None)
            session.pop('koudouID', None)
            session.pop('shosaiID', None)
            return render_template(
                "msg.html",
                title="行動記録編集完了",
                message="行動記録を編集しました。"
            )


@kdu.route("/update3_koudou", methods=['POST'])
def update3_koudou():
    #現在時刻を取得
    dt_now = datetime.now()

    #form変数を受取
    who = request.form['who']
    people_num = request.form['people_num']
    num = int(request.form['num'])
    remarks = request.form['remarks']
    #sessionからshosaiIDを受取
    shosaiID = session["shosaiID"]

    #データベースをオープン
    dbcon, cur = my_open(**dsn)

    #koudou_shosaiテーブルのデータを更新
    sqlstring = f"""
        update koudou_shosai
        set
        who = '{who}',
        people_num = '{people_num}',
        remarks = '{remarks}',
        lastupdate = '{dt_now}'
        where shosaiID = {shosaiID}
        ;
    """
    #クエリを実行
    my_query(sqlstring, cur)
    #テーブルに変更を適用
    dbcon.commit()

    sqlstring = f"""
        select *
        from koudou_friend
        where shosaiID = {shosaiID}
        and delflag = False
        ;
    """
    my_query(sqlstring, cur)

    #テーブルデータをDataFrameに変換
    recset = pd.DataFrame(cur.fetchall())
    if recset.empty:
        recset = None
    print(recset)

    #同大学の同行者が1人以上の時、form_friendに移動
    if num >= 1:
        return render_template(
            "form_friend.html",
            to_url='/update4_koudou',
            title="同行者記録ページ",
            msg="同行者を入力してください",
            num=num,
            friendcode=recset
        )
    #同大学の同行者がいない時、入力を終了
    else:
        sqlstring = f"""
            update koudou_friend
            set
            delflag = True
            where shosaiID = {shosaiID}
        """
        my_query(sqlstring, cur)
        dbcon.commit()
        my_close(dbcon, cur)
        session.pop('num', None)
        session.pop('koudouID', None)
        session.pop('shosaiID', None)
        return render_template(
            "msg.html",
            title="行動記録更新",
            message="行動記録を更新しました。"
        )


@kdu.route("/update4_koudou", methods=['POST'])
def update4_koudou():
    #データベースをオープン
    dbcon, cur = my_open(**dsn)

    #現在時刻を取得
    dt_now = datetime.now()
    #form変数を受取
    num = int(request.form['num'])
    clientcode = session['id']
    #sessionから更新前のnumを受取
    num_old = session["num"]
    #sessionからshosaiIDを受取
    shosaiID = session['shosaiID']
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
            if clientcode == rowdata['clientcode']:
                continue
            elif item == rowdata['clientcode']:
                #clientcodeが一致したらflagを立てる
                flag = 1
        #もしflagが立っていなかったとき、clientcodeに誤り有
        #form_friendで入力しなおし
        if flag == 0:
            return render_template(
                "form_friend.html",
                title="同行者記録ページ",
                msg="学籍番号に誤りがあります。正しい学籍番号を入力してください。",
                num=num,
                friendcode=None
            )

    sqlstring = f"""
        select *
        from koudou_friend
        where shosaiID = {shosaiID}
        and delflag = False
        ;
    """
    my_query(sqlstring, cur)

    recset = pd.DataFrame(cur.fetchall())
    count = 0
    #koudou_friendテーブルにデータを挿入
    if num_old > num:
        for item in friendcode:
            sqlstring = f"""
                update koudou_friend
                set
                shosaiID = '{shosaiID}',
                friendcode = '{item}',
                lastupdate = '{dt_now}'
                where friendID = {recset['friendID'][count]}
                ;
            """
            count += 1
            #クエリを実行
            my_query(sqlstring, cur)
    else:
        for item in friendcode:
            if count >= num_old:
                sqlstring = f"""
                    INSERT INTO koudou_friend
                    (shosaiID, friendcode, lastupdate)
                    values
                    ({shosaiID}, '{item}', '{dt_now}')
                    ;
                """
            else:
                #koudou_friendテーブルのデータを更新
                sqlstring = f"""
                    update koudou_friend
                    set
                    shosaiID = '{shosaiID}',
                    friendcode = '{item}',
                    lastupdate = '{dt_now}'
                    where friendID = {recset['friendID'][count]}
                    ;
                """
            count += 1
            #クエリを実行
            my_query(sqlstring, cur)

    if num_old > num:
        for i in range(num_old - num):
            sqlstring = f"""
                update koudou_friend
                set
                delflag = True,
                lastupdate = '{dt_now}'
                where friendID = {recset['friendID'][count]}
                ;
            """
            my_query(sqlstring, cur)
            count += 1

    #テーブルに変更を適用
    dbcon.commit()
    #データベースをクローズ
    my_close(dbcon, cur)

    session.pop('num', None)
    session.pop('koudouID', None)
    session.pop('shosaiID', None)

    #実行終了
    return render_template(
        "msg.html",
        title="行動記録更新",
        message="行動記録を更新しました。"
    )


@kdu.route("/delete_koudou", methods=['POST'])
def delete_koudou():
    #データベースをオープン
    dbcon, cur = my_open(**dsn)

    #現在時刻を取得
    dt_now = datetime.now()

    #form変数を受取
    koudouID = request.form['koudouID']

    sqlstring = f"""
        update koudou
        set
        lastupdate = '{dt_now}',
        delflag = True
        where koudouID = {koudouID}
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
        title="行動記録削除",
        message="行動記録を削除しました。"
    )
