from crypt import methods
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Flask, render_template, request
from mydblib2 import my_select as select


def flag(str):
    if str == ("Temp_mean" or "Temp_max" or "Temp_min"):
        return "Celsius"
    elif str == "Precipitation":
        return "mm"
    else:
        return "Hours"


app = Flask(__name__, static_folder="static")

# top


@app.route("/")
def index():
    return render_template(
        "TS3-top-T120015.html",
        title="Webプログラミング問題3-T120015",
    )

# /Suwa


@app.route("/Suwa")
def result1():

    sql = f"""
    SELECT *
    FROM weather
    WHERE Area = 'Suwa'
    """
    title = "SuwaのTemp_mean"

    weather = select("wptest", sql)
    result1 = weather.query("1960 <= Year < 2020").groupby(
        "Year", as_index=False).mean()

    path = "/static/TS32-T120015.png"
    plt.plot(result1["Year"], result1["Temp_mean"])
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(flag("Temp_mean"))
    plt.savefig(f".{path}")
    plt.close()

    return render_template(
        "TS3-result-T120015.html",
        title=title,
        image=path
    )


@app.route("/Area/<Area>")
def result2(Area):
    sql = f"""
    SELECT *
    FROM weather
    WHERE Area = '{Area}'
    """
    title = f"{Area}のTemp_mean"

    weather = select("wptest", sql)
    result1 = weather.query("1960 <= Year < 2020").groupby(
        "Year", as_index=False).mean()

    path = "/static/TS33-T120015.png"
    plt.plot(result1["Year"], result1["Temp_mean"])
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(flag("Temp_mean"))
    plt.savefig(f".{path}")
    plt.close()

    return render_template(
        "TS3-result-T120015.html",
        title=title,
        image=path
    )


@app.route("/form")
def form():
    title = "地域,気象データ選択フォーム"
    return render_template(
        "TS3-form-T120015.html",
        title=title,
    )


@app.route("/search", methods=["POST"])
def result3():
    Area = request.form["Area"]
    Data = request.form["Data"]

    sql = f"""
    SELECT *
    FROM weather
    WHERE Area = '{Area}'
    """
    title = f"{Area}の{Data}"

    weather = select("wptest", sql)
    result1 = weather.query("1960 <= Year < 2020").groupby(
        "Year", as_index=False).mean()

    path = "/static/TS34-T120015.png"
    plt.plot(result1["Year"], result1[Data])
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(flag(Data))
    plt.savefig(f".{path}")
    plt.close()

    return render_template(
        "TS3-result-T120015.html",
        title=title,
        image=path
    )


app.run(host="localhost", port=5000, debug=True)
