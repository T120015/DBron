from flask import Flask, render_template as retmp, request
from mydblib2 import my_select as slc
from scipy.stats import f_oneway as fone
from ..Rei0402 import tukey_hsd as th

app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return retmp(
        "index.html",
        title="年代ごとの気象データ一元配置分散分析ページ",
        message="比較する地域と気象データを選択してください."
    )


@app.route("/search", methods=["POST"])
def result():
    area = request.form["Area"]
    data = request.form["Data"]

    sqlstr = """
    SELECT 
    FROM weather
    WHERE AREA = '{}'
    ;
    """.format(area)

    weather = slc("webprog", sqlstr)

    g_f = weather.query("1960 <= Year <= 1979")[data]
    g_s = weather.query("1980 <= Year <= 1999")[data]
    g_t = weather.query("2000 <= Year <= 2019")[data]

    b_val, p_val = fone(g_f, g_s, g_t)

    print(f"一元配置分散分析 p_value={p_val:.3f}")
    if(p_val < 0.05):
        th(["Y1960-", "Y1980-", "Y2000-"],
           g_f, g_s, g_t)


app.run(host="localhost", port=5000, debug=True)
