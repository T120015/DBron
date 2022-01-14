from tkinter import Y
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Flask, render_template as retmp, request
from scipy.stats import ttest_rel as tt
from mydblib2 import my_select as slc

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
    area1 = request.form["Area1"]
    area2 = request.form["Area2"]
    yaer1 = request.form["Yaer1"]
    yaer2 = request.form["Yaer2"]

    sqlstr = f"""
    SELECT Month,Year,Temp_mean
    FROM weather
    WHERE AREA IN ('{area1}', '{area2}')
    """

    weather = slc("webprog", sqlstr)

    mid1 = yaer1 + 10
    mid2 = yaer2 + 10

    result1 = weather.query(
        f" Year >= {yaer1} & Year<{mid1} & Area == {area1}").groupby('Month', as_index=False)['Temp_mean']
    result2 = weather.query(
        f" Year >= {yaer2} & Year<{mid2} & Area == {area2}").groupby('Month', as_index=False)['Temp_mean']

    t_val, p_val = tt(result1, result2)
    print(f"p_value={p_val:.3f}")

    title = f"{area1}{yaer1}年代と{area2}{yaer2}年代の比較"
    path = "/static/En0407.png"
    plt.plot(result1['Month'], result1['Temp_mean'], label=f"{area1}{yaer1}")
    plt.plot(result2['Month'], result2['Temp_mean'], label=f"{area2}{yaer2}")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Temp_mean")
    plt.legend()
    plt.savefig(f".{path}")
    plt.close()

    df = pd.DataFrame([result1["Month"], result1['Temp_mean'],
                      result2['Temp_mean']])

    # print(result1)
    return retmp(
        "result.html",
        title=title,
        message=f"t検定: p_value={p_val: .3f}",
        cols=["月", "Y1960-", "Y1980-", "Y2000-"],
        table_data=df.T.values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
