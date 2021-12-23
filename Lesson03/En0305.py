import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from mydblib import my_select as slc

frm = "post_office"
city = "茅野市"
prefecture = ["長野県", "新潟県", "富山県", "石川県", "福井県"]

sqlstring = f"""
    SELECT prefecture, COUNT(prefecture) AS pcnt
    FROM {frm}
    WHERE prefecture IN('{prefecture[0]}','{prefecture[1]}','{prefecture[2]}','{prefecture[3]}','{prefecture[4]}')
    GROUP BY prefecture
    ;
"""

postNum = slc(sqlstring)
print(postNum)
# make graph
plt.bar(range(len(postNum["prefecture"])), range(len(postNum["pcnt"])),
        ticklabel=postNum["prefecture"])
plt.title("北信越地方県別事業所数")
plt.xlabel("県名")
plt.ylabel("登録数便番号数")
plt.savefig("./img/En0305.png")
