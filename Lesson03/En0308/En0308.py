from flask import Flask, render_template as rt
from werkzeug import datastructures

app = Flask(__name__)

@app.route("/")
def index():
    return rt("top.html", title = "地域", cols = "", msg = "")


@app.route("/city/<city>")
def top(city):
    city = str(city)
    import pandas as pd
    from mydblib import my_select as slc

    sqlstr = f"""
    SELECT *
    FROM post_area
    WHERE city LIKE ('{city}%')
    """

    qdata = slc(sqlstr)

    return rt("top.html", title=city, cols =qdata.columns, msg = qdata.values)


app.run(host="127.0.0.1", port=5000, debug=True)
