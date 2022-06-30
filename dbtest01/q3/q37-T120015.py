#q37

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
    select gakusekicode, namae, sum(atdata) as cnt
    from ga_ka_at
    where classdate like ('2020-04%')
    group by gakusekicode
    ;
"""

my_query(query, cur)
recset = pd.DataFrame(cur.fetchall())
my_close(dbcon, cur)

print(recset)
