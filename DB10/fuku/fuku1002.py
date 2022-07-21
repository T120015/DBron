#fuku1002.py 
#FlaskモジュールでDBの操作
from crypt import methods
from MyDatabase import my_open , my_query , my_close
import pandas as pd

#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'sampledb' #オープンするデータベース名
}

from flask import Flask,render_template ,request
#Flaskのコンストラクタ
app = Flask(__name__ ,static_folder="static")

#ルーティング定義
@app.route("/")
def top():
    return render_template( "fuku1002-top.html",
    
        title = "郵便番号検索" 
    )

@app.route("/search", methods=['post'])
def search():
    #form変数の受け取り
    city = request.form["city"]
    sel = request.form["sel"]

    #DBオープン
    dbcon,cur = my_open(**dsn)
    
    if sel == "area" :
        #データ挿入のためのSQL文
        sqlstring = f"""
            SELECT *
            FROM post_area
            WHERE city LIKE '%{city}%'
            ;
        """
        kensaku = "地域別郵便番号"
    else:
        sqlstring = f"""
            SELECT *
            FROM post_office
            WHERE city LIKE '%{city}%'
            ;
        """
        kensaku = "事業所別郵便番号"
    #クエリ実行
    my_query(sqlstring,cur)
    recset = pd.DataFrame(cur.fetchall())

    #データベースクローズ
    my_close(dbcon,cur)

    return render_template( "fuku1002-table.html",
        title = f"{city} {kensaku}の検索結果",
        table_data = recset    
    )

#プログラム起動
app.run(host="localhost",port=5000,debug=True)
