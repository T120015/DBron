from flask import Flask,render_template

#Flaskのコンストラクタ
app = Flask(__name__)

#ルーティング定義
@app.route("/")
def top():
    return "Hello Flask world"

@app.route("/samp01/")
def top2():
    #render_templateにより，templatesフォルダのtop.htmlを呼び出し
    return render_template("top.html")

@app.route("/samp02/")
def top3():
    #render_templateにより，templatesフォルダのtop2.htmlを呼び出し
    return render_template("top2.html",
        title="これはtop2.htmlです",
        message="top2.htmlをテンプレートして読み込んでいます。"
    )

@app.route("/samp02/<msg>")
def top4(msg):
    #render_templateにより，templatesフォルダのtop2.htmlを呼び出し
    return render_template("top2.html",
        title="メッセージの受け渡し",
        message=msg
    )

#プログラム起動
app.run(host="localhost",port=5000,debug=True)

