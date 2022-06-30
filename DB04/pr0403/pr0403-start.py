from datetime import datetime as dt  # uses time
from MyDatabase import my_open, my_query, my_close  # use Database
import pandas as pd  # make DataFrame

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron04'
}


def df_Start():
    dbcon, cur = my_open(**dsn)
    sqlstr = f"""USE dbron04;
        DROP TABLE if NOT EXISTS myfriends;
        CREATE TABLE myfriends(
        friendsID INT NOT NULL AUTO_INCREMENT,
        fname VARCHAR(32) NOT NULL,
        age INT NOT NULL,
        gender VARCHAR(8) NOT NULL,
        tell VARCHAR(32),
        email VARCHAR(64),
        lastupdate VARCHAR(64) NOT NULL,
        delflag BOOL NOT NULL default FALSE,
        PRIMARY KEY(friendsID)
    );
    """
    my_query(sqlstr, cur)
    tmp = pd.DataFrame(cur.fetchall())
    my_close(dbcon, cur)
    print(tmp)
    

    df: pd.DataFrame = pd.read_csv(
        "./data/friends.csv", dtype={'tell': 'str'}, header=0)

    dt_now = dt.now()
    dbcon, cur = my_open(**dsn)
    for key, val in df.iterrows():
        sqlstr = f"""
        INSERT INTO myfriends
        (fname, age, gender, tell, email, lastupdate)
        VALUES
        ('{val[0]}',{val[1]},'{val[2]}','{val[3]}','{val[4]}','{dt_now}')
        ;
        """
        my_query(sqlstr, cur)
        dbcon.commit()

    my_close(dbcon, cur)
    exit()


df_Start()
