from flask import Blueprint, render_template, request, session, redirect, url_for
from MyDatabase import my_open, my_query, my_close
from datetime import date

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron'  # オープンするデータベース名
}

cnt = Blueprint('cnt', __name__)


@cnt.route("/")
def top():
    # トップページ
    return render_template(
        "top.html", title="メインメニュー", msg="main src", school=session["school"]
    )


@cnt.route("/infect_corona")
def infect():
    return render_template(
        "form_infect.html",
        title="コロナ感染記録",
        today=date.today()
    )


@cnt.route("/infect_corona1", methods=["POST"])
def infect1():
    code = session["id"]
    onset = request.form["onset"]
    infect = request.form["infect"]
    #感染者 or 接触者の判定
    if int(infect) == 1:
        #病院の記録を追加
        hospital = request.form["hospital"]
    else:
        hospital = None

    print(hospital)
    
    dbcon, cur = my_open(**dsn)

    sql = f"""
        INSERT INTO corona
        (clientcode,judge, hospital, onset)
        VALUES
        ('{code}',{infect},'{hospital}','{onset}')
        ;
    """
    #SQLに書き込み
    my_query(sql, cur)
    #SQLに反映
    dbcon.commit()
    my_close(dbcon, cur)
    #メッセージを表示
    return render_template(
        "msg.html",
        title="コロナ陽性・濃厚接触者記録",
        message="感染記録を保存しました"
    )
