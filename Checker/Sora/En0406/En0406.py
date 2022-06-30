# En0406
from flask import Flask, render_template, request
# Flaskのコンストラクタ
app = Flask(__name__, static_folder="static")

# ルーティング定義


@app.route("/")
def top():
    return render_template(
        "top.html",
        title="年代ごとの気象データ一元配置分散分析ページ"
    )

# 地点と年度を選択するフォーム


@app.route("/search", methods=["POST"])
def top2():
    Area = request.form["Area"]
    Temp = request.form["Temp"]
    # print( f"Area ={Area}") #for debug
    # print( f"Temp ={Temp}") #for debug

    # データベースを引数で指定できるバージョン
    import pandas as pd
    from mydblib2 import my_select

    # SQLの設定
    # tableに検索するtable名
    sqlstring = f"""
        SELECT Month,{Temp}, Year
        FROM weather
        WHERE Area = '{Area}'
        ;
    """
    # webprogデータベースのweatherテーブルのレコードを読み込み
    weather = my_select("webprog", sqlstring)
    title = f"{Area}{Temp}の一元配置分散の結果"

    # Yearをrequestしてないので、SQL文にYear必須
    print(f"平均値 \n{weather.groupby('Month').mean()}")
    g_Y1960 = weather.query("Year <= 1979").groupby('Month').mean()[Temp]
    g_Y1980 = weather.query("1979 < Year < 2000").groupby('Month').mean()[Temp]
    g_Y2000 = weather.query("Year > 1999").groupby('Month').mean()[Temp]
    print(f"g_Y1980 {g_Y1980}")  # for Debug
    #print(f"g_Y1980.gruopby {g_Y1980.groupby('Month').mean()}")

    def tukey_hsd(ind, *args):
        import pandas as pd
        import numpy as np
        from statsmodels.stats.multicomp import pairwise_tukeyhsd

        data_arr = np.hstack(args)
        ind_arr = np.array([])
        for x in range(len(args)):
            ind_arr = np.append(ind_arr, np.repeat(ind[x], len(args[x])))
        return pairwise_tukeyhsd(data_arr, ind_arr)

    # 手順(1)3つ以上の母集団の平均値の検定は，1元配置分散分析 f_oneway を行う
    from scipy.stats import f_oneway
    # b_val(検定値)，p_val(p値：有意水準　0.05未満なら分散が等しくない)
    b_val, p_val = f_oneway(g_Y1960, g_Y1980, g_Y2000)

    import matplotlib.pyplot as plt
    import japanize_matplotlib
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    plt.plot(month, g_Y1960, label="Y1960")
    plt.plot(month, g_Y1980, label="Y1960")
    plt.plot(month, g_Y2000, label="Y1960")
    plt.title(title)
    plt.xlabel("月")
    plt.ylabel("温度")
    plt.savefig("./static/En0406.png")
    plt.close()

    df = pd.DataFrame([month, g_Y1960, g_Y1980, g_Y2000])

    return render_template(
        "search.html",
        title=title,
        message=f"一元配置分散分析 p_value={p_val:.3f}",
        redata=tukey_hsd(["g_Y1960", "g_Y1980", "g_Y2000"],
                         g_Y1960, g_Y1980, g_Y2000),
        cols=["月", "Y1960-", "Y1980-", "Y2000-"],  # 列（項目）
        table_data=df.T.values,
        image="/static/En0406.png"
    )


# プログラム起動
app.run(host="localhost", port=5000, debug=True)
