from flask import Flask as flk,render_template as rndtmp


app = flk(__name__)

@app.route("/")
def top():
  return "ようこそ素数の世界へ"

@app.route("/sosuu/")
def index():

  return rndtmp("index.html",title="10までの素数")

app.run(host="127.0.0.1",port=5000)