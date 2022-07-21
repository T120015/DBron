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

    sqlstr = f"""
    SELECT Month,Year,{data}
    FROM weather
    WHERE AREA = '{area}'
    ;
    """

    weather = slc("webprog", sqlstr)
    #query(Year >= 1960 & Year < 1980)
    result1 = weather.query(
        "1960 <= Year < 1980").groupby('Month', as_index=False).mean()
    result2 = weather.query(
        "1980 <= Year < 2000").groupby('Month', as_index=False).mean()
    result3 = weather.query(
        "2000 <= Year < 2020").groupby('Month', as_index=False).mean()

    b_val, p_val = fone(result1[data], result2[data], result3[data])
    msg = (f"一元配置分散分析 p_value={p_val:.3f}")
    redata = th(["Y1960-", "Y1980-", "Y2000-"],
                result1[data], result2[data], result3[data])
    title = f"{area},{data}の一元配置分散分析結果"
    path = "/static/En0406.png"
    plt.plot(result1['Month'], result1[data], label="Y1960-")
    plt.plot(result2['Month'], result2[data], label="Y1980-")
    plt.plot(result3['Month'], result3[data], label="Y2000-")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(data)
    plt.legend()
    plt.savefig(f".{path}")
    plt.close()
    # サポート Byじまくん
    df = pd.DataFrame([result1["Month"], result1[data],
                      result2[data], result3[data]])
    #array[key] = value
    return retmp(
        "result.html",
        title=title,
        message=msg,
        redata=redata,
        cols=["月", "Y1960-", "Y1980-", "Y2000-"],
        table_data=df.T.round(1).values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
