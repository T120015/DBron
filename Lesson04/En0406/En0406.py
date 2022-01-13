from flask import Flask, render_template as retmp, request
from mydblib2 import my_select as slc

app = Flask(__name__, static_folder="static")


@app.route("/")
def top():
    return retmp(
        "index.html",
        title="年代ごとの気象データ一元配置分散分析ページ"
    )


app.run(host="127.0.0.1", port=5000, debug=True)
