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
    year1 = request.form["Year1"]
    year2 = request.form["Year2"]

    sqlstr = f"""
    SELECT *
    FROM weather
    WHERE AREA IN ('{area1}', '{area2}')
    """

    weather = slc("webprog", sqlstr)

    mid1 = str(int(year1) + 10)
    mid2 = str(int(year2) + 10)

    result1 = weather.query(
        f" Year >= {year1} & Year<{mid1}").groupby('Month', as_index=False).mean()
    result2 = weather.query(
        f" Year >= {year2} & Year<{mid2}").groupby('Month', as_index=False).mean()

    t_val, p_val = tt(result1["Temp_mean"], result2["Temp_mean"])
    print(f"p_value={p_val:.3f}")
    name1 = f"{area1}{year1}年代"
    name2 = f"{area2}{year2}年代"

    title = f"{name1}と{name2}の比較"
    path = "/static/En0407.png"
    plt.plot(result1['Month'], result1['Temp_mean'], label=name1)
    plt.plot(result2['Month'], result2['Temp_mean'], label=name2)
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Temp_mean")
    plt.legend()
    plt.savefig(f".{path}")
    plt.close()

    df = pd.DataFrame([result1["Month"], result1['Temp_mean'],
                      result2['Temp_mean']])

    message = f"t検定: p_value={p_val: .3f}"
    if (p_val < 0.05):
        message += "‐有意差あり"
    else:
        message += "‐有意差なし"
    # print(result1)
    return retmp(
        "result.html",
        title=title,
        message=message,
        cols=["Month", name1, name2],
        table_data=df.T.values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
