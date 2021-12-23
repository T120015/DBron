import pandas as pd
import mydblib as mdb

frm = "post_area"
city = "茅野市"
prefecture = "長野県"

sqlstring = f"""
    SELECT *
    FROM {frm}
    WHERE city LIKE '%{city}%'
    AND prefecture = '{prefecture}'
    ;
"""
postNum = mdb.my_select(sqlstring)
print(postNum)