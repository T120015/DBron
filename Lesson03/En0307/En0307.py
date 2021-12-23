from flask import Flask as flk,render_template as rndtmp
from sympy import sieve as sv

app = flk(__name__)

@app.route("/")
def top():
  return "ようこそ素数の世界へ"

@app.route("/sosuu/")
def index():
  print([i for i in sv.primerange(10)])
  return rndtmp("index.html",title="10までの素数")

app.run(host="127.0.0.1",port=5000)