# モジュールの役割
import pandas as pd  # データフレーム
import matplotlib.pyplot as plt  # グラフ生成
import japanize_matplotlib  # グラフの日本語化
from flask import Flask, render_template as retmp, request  # ブラウザ生成
from scipy.stats import f_oneway as fone  # 分散分析
from mydblib2 import my_select as slc  # SQL呼び込み
from tukey import tukey_hsd as th  # 検定

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
    area = request.form["Area"]
    data = request.form["Data"]

    sqlstr = f"""
    SELECT Month,Year,{data}
    FROM weather
    WHERE AREA = '{area}'
    ;
    """
    # SQLからの読み込み
    weather = slc("webprog", sqlstr)
    # 各年ごとのデータをそれぞれに格納
    #query() - 条件を満たすデータを抽出
    #groupby() - 指定されたラベルでグループ化
    result1 = weather.query(
        "1960 <= Year < 1980").groupby('Month').mean()
    result2 = weather.query(
        "1980 <= Year < 2000").groupby('Month').mean()
    result3 = weather.query(
        "2000 <= Year < 2020").groupby('Month').mean()
    # 月のリスト
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # 分散分析
    b_val, p_val = fone(result1[data], result2[data], result3[data])
    msg = (f"一元配置分散分析 p_value={p_val:.3f}")
    # 検定結果
    redata = th(["Y1960-", "Y1980-", "Y2000-"],
                result1[data], result2[data], result3[data])
    # グラフ
    title = f"{area},{data}の一元配置分散分析結果"
    path = "/static/En0406.png"  # 画像の保存先とファイル名
    # 各年ごとのデータをプロット
    plt.plot(month, result1[data], label="Y1960-")
    plt.plot(month, result2[data], label="Y1980-")
    plt.plot(month, result3[data], label="Y2000-")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(data)
    plt.legend()  # plotのlabel(凡例)を適応
    plt.savefig(f".{path}")
    plt.close()
    # 新たにデータ化
    df = pd.DataFrame([month, result1[data],
                      result2[data], result3[data]])
    # htmlに代入
    return retmp(
        "result.html",
        title=title,
        message=msg,
        redata=redata,
        cols=["月", "Y1960-", "Y1980-", "Y2000-"],
        table_data=df.T.round(1).values,
        image=path
    )
    # dfを転置(.T)して小数点第1位で四捨五入(.raoud(1))した
    # 要素(.values)をtable_dataに代入


# コンストラクタを実行
app.run(host="localhost", port=5000, debug=True)
