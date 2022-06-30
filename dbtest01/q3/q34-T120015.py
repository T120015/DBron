# q34

from MyDatabase import my_open, my_query, my_close
import pandas as pd

dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbtest01'
}

dbcon, cur = my_open(**dsn)

query = f"""
    select *
    from ga_ka_at
    where kamokucode = 'J002'
    ;
"""

my_query(query, cur)
recset = pd.DataFrame(cur.fetchall())
my_close(dbcon, cur)

#print(recset)

data = recset.loc[:,['gakusekicode', 'namae', 'classdate', 'atdata']]

result = pd.pivot_table(
    data, index=['gakusekicode','namae'], columns='classdate'
)

print(result)