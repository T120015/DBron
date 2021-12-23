#例題4　SELECTの例(cursorの作成時 dictonary=True)

import pandas as pd
from mydblib import my_select

#SQLの設定
# tableに検索するtable名
city="原村"
prefecture = "長野県"
sqlstring =  f"""
    SELECT *
    FROM post_area
    WHERE city LIKE '%{city}%'
    AND prefecture = '{prefecture}'
    ;
"""

post_number = my_select( sqlstring )
print( post_number ) #for debug
