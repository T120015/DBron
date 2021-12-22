import os
from flask import Flask,render_template

#Flaskのコンストラクタ
app = Flask(__name__)

#ルーティング定義
@app.route("/")
def top():
    return "Hello Flask world"

@app.route("/test01/")
def top2():
    #render_templateにより，templateフォルダのindex.htmlを呼び出し
    return render_template("top2.html",
        title="これはテストtitle",
        message="Jinjaのメッセージテスト"
    )

@app.route("/test01/<int:aa>",methods=["GET"])
def top3(aa):
    return f"Hello aaa わかった！{aa} "


@app.route("/test02/")
def sub():
    import numpy as np
    a = np.random.randint(1,7,10)
    mean = np.mean(a)
    std = np.std(a)

    MESSAGE = f"""
        乱数を発生した結果 \n{a}\n
        平均値は{mean}
        標準偏差は{std}
    """
    return render_template("top2.html",
        title = "numpy no 乱数",
        message = MESSAGE
    )

#プログラム起動
app.run(host="localhost",port=5000,debug=True)

