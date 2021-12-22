from flask import Flask,render_template

#Flaskのコンストラクタ
app = Flask(__name__)

#ルーティング定義
@app.route("/")
def top():
    return "郵便番号検索ページ"

@app.route("/yuubin/<city>")
def top1(city):
    import pandas as pd
    from mydblib import my_select

    #post_areaのcityに対応するレコードを抽出する処理
    sqlstring = f"""
        SELECT *
        FROM post_area
        WHERE city = '{city}'
        ;
    """
    #DBの検索結果は，qdata(pandas DataFrame形式) に入る
    qdata = my_select( sqlstring )
    #print(f"qdata \n{qdata}")     #for debug

    return render_template("top.html",
        city = city,
        cols = qdata.columns,
        table_data = qdata.values
    )

#プログラム起動
app.run(host="localhost",port=5000,debug=True)