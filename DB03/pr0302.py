from MyDatabase import my_query, my_close, my_open
#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',  # mysqlの接続ポート番号
    'user': 'root',  # dbアクセスするためのユーザid
    'password': '1234',  # ユーザidに対応するパスワード
    'database': 'dbron03'  # オープンするデータベース名

}

dbcon, cur = my_open(**dsn)

#テーブルmeibo02を作成する。
my_query("DROP TABLE if EXISTS meibo03;", cur)
sqlstring = f"""
    CREATE TABLE meibo03(
        meibo03ID int not null auto_increment,
        namae varchar(32),
        email varchar(64),
        postnumber varchar(16),
        postaddress varchar(128),
        primary key(meibo03ID)
    );
"""
my_query(sqlstring, cur)

#テーブル構造の表示
my_query("DESC meibo03", cur)
print("result: DESC meibo03;")
for col in cur:
    print(col)

#カーソルとDBコンソールのクローズ
my_close(dbcon, cur)
