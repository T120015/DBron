import pandas as pd
import mydblib as mdb

frm = "post_office"
city = "茅野市"
prefecture = "長野県"

sqlstring = f"""
    SELECT *
    FROM {frm}
    WHERE city ='{city}'
    AND prefecture = '{prefecture}'
    ;
"""
postNum = mdb.my_select(sqlstring)
#.iterrows:配列を1行を繰り返す
for row in postNum.iterrows():
  print("{} {} {}".format(row["postnumber"],row["officename"],row["area"]))
