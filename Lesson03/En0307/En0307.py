from flask import Flask as flk, render_template as rndtmp
from numpy.lib.function_base import append
from sympy import isprime as ip
import numpy as np

app = flk(__name__)


@app.route("/")
def top():
    return "ようこそ素数の世界へ"


@app.route("/sosuu/")
def index():
    num = []
    for i in range(10):
        if ip(i):
            print(i)
            num.append(i)
    return rndtmp('index.html', title="10までの素数", msg=num)


app.run(host="127.0.0.1", port=5000, debug=True)
