import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Flask, render_template, request


def select(db, sqlstr):
    import mysql.connector as mydb
    import sys

    try:
        dbcon = mydb.connect(
            host='webprog_db',
            port='3306',
            user='root',
            password='1234',
            database=db
        )
        cur = dbcon.cursor(dictionary=True)

    except mydb.Error as e:
        print(f"DBコネクションエラー\n{e}")
        sys.exit()
    try:
        cur.execute(sqlstr)
        recset = cur.fetchall()
    except mydb.Error as e:
        print(f"クエリ実行エラー\n{e}")
        print(f"入力されたSQLは\n{sqlstr}")
        sys.exit()

    return pd.DataFrame(recset)


app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="自作テンプレート",
    )


@app.route("/result", methods=["POST"])
def result():
    area = request.form["Area"]

    sql = f"""
    SELECT *
    FROM weather
    WHERE Area = '{area}'
    """

    weather = select('webprog', sql)
    result1 = weather.groupby('Month', as_index=False).mean()
    result2 = weather.groupby('Month', as_index=False).std()
    df = pd.DataFrame([result1['Month'],
                      result1['Temp_mean'], result2['Temp_mean']])
    print(df)

    title = f"{area}の月別平均気温"
    path = "/static/image.png"
    plt.plot(result1["Month"], result1["Temp_mean"])
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Temp_mean")
    plt.savefig(f".{path}")

    return render_template(
        "result.html",
        title=title,
        colms=["Month", "Mean", "Std"],
        table_data=df.T.round(1).values,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
