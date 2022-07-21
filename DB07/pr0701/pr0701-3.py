from werkzeug.datastructures import FileStorage
import chardet
import pandas as pd
from MyDatabase import my_open, my_query, my_close
from flask import Flask, render_template, request
from datetime import datetime as dt
# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")
# ファイル最大サイズを16MByteに設定
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def top():
    return render_template(
        "pr0701-top_form.html",
        title="出席CSVファイルアップロード画面"
    )

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron07'
}

@app.route("/upload_csv", methods=["POST"])
def uplaod_csv():
    # csvファイルの受け取り
    csv_data = request.files["upfile"]
    print(csv_data)  # for debug

    # CSVデータをDataFrameとして読み込み
    df = pd.read_csv(csv_data, header=0)
    print(df)  # for debug


    dbcon, cur = my_open(**dsn)
    dt_now = dt.now()
    for ind, data in df.iterrows():
        query = f"""
            INSERT INTO seki
            (s_code,jcnt,sekidata,lastupdate)
            VALUES
            ('{data['s_code']}',{data['jcnt']},{data['sekidata']},'{dt_now}')
            ;
        """
        my_query(query, cur)
    msg = f"{len(df)}レコードを新規挿入しました"
    print(msg)
    dbcon.commit()

    my_close(dbcon, cur)

    return render_template("pr0701-table.html",
                           title=msg,
                           filename=f"アップされたファイル名 {csv_data.filename}",
                           table_data=df
                           )

@app.route("/kakunin")
def checker():
    dbcon, cur = my_open(**dsn)
    query = f"""
        select *
        from std_seki
    """
    my_query(query,cur)
    recset = pd.DataFrame(cur.fetchall())
    data = recset.loc[:,['s_code','namae','jcnt','sekidata']]
    result = pd.pivot_table(
        recset, index=['s_code', 'namae'], columns='jcnt'
    )

    return render_template(
        "pr0701-msg.html",
        title = "出席の集計",
        message = result
    )

# プログラム起動
app.run(host="localhost", port=5000, debug=True)
