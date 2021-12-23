from flask import Flask as flk, render_template as rndtmp
from sympy import isprime as ip

app = flk(__name__)


@app.route("/")
def top():
    return "ようこそ素数の世界へ"


@app.route("/sosuu/")
def index():
    num = []
    for i in range(10):
        if ip(i):
            num.append(i)
    msg = """
    素数は{}です.
    """.format(num)
    return rndtmp('top.html', title="10までの素数", msg=msg)


@app.route("/sosuu/<n>")
def Number(n):
    num = []
    for i in range(int(n)+1):
        if ip(i):
            num.append(i)
    msg = """
    素数は{}です．
    """.format(num)
    return rndtmp('top.html', title="{}までの素数".format(n), msg=msg)


app.run(host="127.0.0.1", port=5000, debug=True)
