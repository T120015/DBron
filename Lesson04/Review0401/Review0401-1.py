# 復習問題 0401　Flaskモジュールで，DBアクセス&データ分析
# このプログラムは，グラフファイルを出力するので，実行するディレクトリが重要
# Review0401.pyが存在するフォルダを，カレントディレクトリとして実行する

from flask import Flask, render_template
# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")

# ルーティング定義


@app.route("/")
def top():
    return render_template("Review0401.html",
                           title="復習問題01",
                           message="FlaskでDBアクセス&データ分析",
                           image=""
                           )

# 塾cramごとの，平均値と標準偏差


@app.route("/cram/")
def top2():
    # 例題XXX　t検定
    import pandas as pd
    # データベースを引数で指定できるバージョン
    from mydblib2 import my_select

    # SQLの設定
    # tableに検索するtable名
    sqlstring = """
        SELECT *
        FROM siken1
        ;
    """
    # webprogデータベースのsiken1テーブルのレコードを読み込み
    siken = my_select("webprog", sqlstring)
    # print(f"siken \n{siken}")  # for debug
    # cram英語塾に行っている人と行っていない人に分けて(groupby)して，平均値meanを計算
    # 【入力】
    result1 = siken.groupby("cram").mean()
    # print(f"result1 \n{result1}")  #for debug
    # 【入力】
    result2 = siken.groupby("cram").std()
    # print(f"result2 \n{result2}")  #for debug
    # 【入力】
    # テンプレートに引き渡すための文字列
    # 【入力】
    data = "平均値:{}\n標準偏差:{}\n".format(result1['score'], result2['score'])
    # print(f"msg \n {msg}")   #for debug
    # 棒グラフ
    import matplotlib.pyplot as plt
    import japanize_matplotlib

    plt.bar(range(2),result1['score'],tick_label=["英語塾","行っていない"])
    plt.title("塾による平均値の違い")
    plt.xlabel("部活")
    plt.ylabel("")
    plt.savefig("./static/Review0401-1.png")
    plt.close()

    # render_templateにより，templateフォルダのindex.htmlを呼び出し
    return render_template("Review0401.html",
                           title="部活による違い",
                           message=data,
                           image="/static/Review0401-1.png"
                           )


# プログラム起動
app.run(host="localhost", port=5000, debug=True)
