import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Flask, render_template as retmp, request
from scipy.stats import f_oneway as fone
from mydblib2 import my_select as slc
from tukey import tukey_hsd as th

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
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    sqlstr = f"""
    SELECT Month,Year,{data}
    FROM weather
    WHERE AREA = '{area}'
    ;
    """

    weather = slc("webprog", sqlstr)

    result1 = weather.query(
        " Year >= 1960 & Year < 1980").groupby('Month').mean()
    print(weather.columns)

    g_f = weather.query(" Year >= 1960 & Year < 1980")[data]
    g_s = weather.query(" Year >= 1980 & Year < 2000")[data]
    g_t = weather.query(" Year >= 2000 & Year < 2020")[data]

    b_val, p_val = fone(g_f, g_s, g_t)
    print(f"一元配置分散分析 p_value={p_val:.3f}")
    redata = th(["Y1960-", "Y1980-", "Y2000-"],
                g_f, g_s, g_t)
    title = f"{area},{data}の一元配置分散分析結果"
    path = "/static/En0406.png"
    plt.plot(month, result1[data], label="Y1960-")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(data)
    plt.savefig(f".{path}")
    plt.close()

    return retmp(
        "result.html",
        title=title,
        message=f"一元配置分散分析: p_value={p_val: .3f}",
        redata=redata,
        cols=weather.groupby('Year').mean().columns,
        table_data=result1.values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
