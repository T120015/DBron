import pandas as pd
from mydblib import my_select as slc

frm = "post_office"
city = "茅野市"
prefecture = ["長野県","新潟県","富山県","石川県","福井県"]

sqlstring = f"""
    SELECT *
    FROM {frm}
    AND prefecture IN('{prefecture}')
    ;
"""
postNum = slc(sqlstring)
#index, row = df.iterrows()１行ずつ繰り返す
for index, row in postNum.iterrows():
  print("{} {} {}".format(row["postnumber"], row["officename"], row["area"]))
