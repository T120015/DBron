from datetime import datetime as dt  # uses time
from MyDatabase import my_open, my_query, my_close  # use Database
import pandas as pd  # make DataFrame
from flask import Flask, render_template, request  # start web script
app = Flask(__name__, static_folder="static")  # Constructor


# define Data Souce Name
dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron04'
}


# index


@app.route("/")
def index():
    return render_template(
        "pr0403-index.html",
        title="アドレス帳メンテナンス",
    )

# show Table Data


@app.route("/table-list")
def list():
    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
    SELECT *
    FROM myfriends
    ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "pr0403-table.html",
        title="myfriendsテーブル レコード一覧",
        table_data=recset,
        flag=0
    )

# insert Recode Data


@app.route("/data-insert")
def insert1():
    return render_template(
        "pr0403-insert.html",
        title="myfriendsテーブル レコード挿入"
    )

# tell you finished to insert


@app.route("/msg-insert", methods=["post"])
def insert2():
    dbcon, cur = my_open(**dsn)
    # receive form values
    name = request.form["fname"]
    age = request.form["age"]
    gender = request.form["gender"]
    tell = request.form["tell"]
    email = request.form["email"]

    # get now time
    dt_now = dt.now()

    sqlstring = f"""
    INSERT INTO myfriends
    (fname, age, gender, tell, email, lastupdate)
    VALUES
    ('{name}',{age},'{gender}','{tell}','{email}','{dt_now}')
    ;
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)
    msg = f"{cur.rowcount}件のレコードを追加しました."

    return render_template(
        "pr0403-msg.html",
        title="レコード挿入 完了",
        msg=msg
    )

# updata recode


@app.route("/table-updata")
def updata1():
    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
    SELECT *
    FROM myfriends
    ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "pr0403-table.html",
        title="friendsテーブル レコードの一覧",
        table_data=recset,
        flag=1
    )


@app.route("/data-update", methods=["post"])
def updata2():
    dbcon, cur = my_open(**dsn)
    friendID = request.form["friendsID"]

    # レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT *
        FROM myfriends
        WHERE friendsID = {friendID}
        ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())
    # DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    rowdata = pd.Series(recset.iloc[0])

    my_close(dbcon, cur)
    return render_template(
        "pr0403-update.html",
        title=f"friendID{friendID} 更新",
        table_data=rowdata
    )


@app.route("/msg-update", methods=["post"])
def updata3():
    dbcon, cur = my_open(**dsn)
    id = request.form["friendsID"]
    name = request.form["fname"]
    age = request.form["age"]
    gender = request.form["gender"]
    tell = request.form["tell"]
    email = request.form["email"]
    # 更新日時取得
    import datetime
    dt_now = datetime.datetime.now()

    # レコード更新のsql
    sqlstring = f"""
        UPDATE myfriends
        SET fname = '{name}',
            age = '{age}',
            gender = '{gender}',
            tell = '{tell}',
            email = '{email}',
            lastupdate = '{dt_now}'
        WHERE friendsID = {id}
    """
    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template("pr0403-msg.html",
                           title="レコード更新完了",
                           msg=f"friendID {id}のレコードを更新しました"
                           )


# delete recode
@app.route("/table-delete")
def delete1():
    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
    SELECT *
    FROM myfriends
    ;
    """
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    return render_template(
        "pr0403-table.html",
        title="friendsテーブル レコードの一覧<br>削除するレコードを選択してください.",
        table_data=recset,
        flag=2
    )


@app.route("/msg-delete", methods=["post"])
def delete2():
    # friensIDの取得
    id = request.form["friendsID"]

    # 更新日時取得
    dt_now = dt.now()

    dbcon, cur = my_open(**dsn)

    sqlstring = f"""
        UPDATE myfriends
        SET delflag = 1,
            lastupdate = '{dt_now}'
        WHERE friendsID = {id}
        """

    my_query(sqlstring, cur)
    dbcon.commit()
    my_close(dbcon, cur)

    return render_template(
        "pr0403-msg.html",
        title="レコード削除フラグ",
        msg=f"friendID{id}の削除フラグを更新しました．"
    )


# start web script
app.run(host='127.0.0.1', port=5000, debug=True)
