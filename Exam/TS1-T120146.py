import pandas as pd
from mydblib2 import my_select

print("T120146 小問番号2")

sqlstring =  f"""
    SELECT *
    FROM iris
    ;
"""

iris = my_select( "wptest", sqlstring )

aveiris = iris.groupby("kinds").mean()
sdiris = iris.groupby("kinds").std()

print("平均値")
print(aveiris)
print("標準偏差")
print(sdiris)

import matplotlib.pyplot as plt

df = aveiris.query("kinds == 'setosa'")["petallength"].to_list()
df += aveiris.query("kinds == 'versicolor'")["petallength"].to_list()
df += aveiris.query("kinds == 'virginica'")["petallength"].to_list()




plt.bar(range(len(df)),df,tick_label=["setosa","versicolor","virginica"])
plt.title(f"petallength n={len(iris)}")
plt.xlabel("kinds")
plt.ylabel("mm")
plt.savefig("TS1-T120146.png")