# モジュールの役割
import pandas as pd  # データフレーム
import matplotlib.pyplot as plt  # グラフ生成
import japanize_matplotlib  # グラフの日本語化
from flask import Flask, render_template as retmp, request  # ブラウザ生成
from scipy.stats import ttest_rel as tt  # 検定
from mydblib2 import my_select as slc  # SQL呼び込み

# コンストラクタの生成
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
    # SQLからの読み込み
    weather = slc("webprog", sqlstr)
    # yearがstring型だからint型にキャスト
    mid1 = int(year1) + 10
    mid2 = int(year2) + 10
    # 各年ごとのデータをそれぞれに格納
    #query() - 条件を満たすデータを抽出
    #groupby() - 指定されたラベルでグループ化
    result1 = weather.query(
        f" Year >= {year1} & Year<{mid1} & Area == '{area1}'").groupby('Month').mean()
    result2 = weather.query(
        f" Year >= {year2} & Year<{mid2} & Area == '{area2}'").groupby('Month').mean()
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    name1 = f"{area1}{year1}年代"
    name2 = f"{area2}{year2}年代"
    # 検定
    t_val, p_val = tt(result1["Temp_mean"], result2["Temp_mean"])
    # グラフ
    title = f"{name1}と{name2}の比較"
    path = "/static/En0407.png"  # 画像の保存先とファイル名
    # 各年ごとのデータをプロット
    plt.plot(month, result1['Temp_mean'], label=name1)
    plt.plot(month, result2['Temp_mean'], label=name2)
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Temp_mean")
    plt.legend()  # plotのlabel(凡例)を適応
    plt.savefig(f".{path}")
    plt.close()
    # 新たにデータ化
    df = pd.DataFrame([month, result1['Temp_mean'],
                      result2['Temp_mean']])

    message = f"t検定: p_value={p_val}"
    if (p_val <= 0.05):
        message += "‐有意差あり"
    else:
        message += "‐有意差なし"
    # htmlに代入
    return retmp(
        "result.html",
        title=title,
        message=message,
        cols=["Month", name1, name2],
        table_data=df.T.round(1).values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
