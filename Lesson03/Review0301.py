# 復習問題0301
from os import pwrite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# 試験結果
siken = pd.DataFrame(
    [[62, 56, 50], [79, 72, 100], [0, 15, 49], [44, 71, 56], [62, 44, 76], [31, 46, 56], [65, 87, 51], [14, 35, 15], [1, 21, 27],
     [54, 62, 28], [25, 51, 17], [55, 62, 48], [16, 45, 43], [67, 85, 29], [
         6, 32, 49], [94, 100, 66], [37, 24, 24], [41, 14, 37],
     [90, 92, 57], [47, 77, 41], [8, 17, 65], [27, 37, 15], [1, 22, 0], [
        24, 23, 32], [99, 91, 90], [28, 53, 65], [31, 34, 39],
     [62, 63, 92], [61, 30, 39], [89, 64, 60], [18, 42, 10], [35, 14, 75], [
        77, 63, 69], [57, 70, 69], [18, 22, 44], [54, 76, 21],
     [34, 15, 27], [38, 67, 30], [12, 17, 4], [18, 0, 50], [66, 89, 87], [90, 87, 93], [19, 52, 19], [80, 86, 63], [42, 55, 14]],
    columns=["Math", "Eng", "Jpn"],
    index=["H001", "H002", "H003", "H004", "H005", "H006", "H007", "H008", "H009", "H010", "H011", "H012", "H013",
           "H014", "H015", "H016", "H017", "H018", "H019", "H020", "H021", "H022", "H023", "H024", "H025", "H026", "H027",
           "H028", "H029", "H030", "H031", "H032", "H033", "H034", "H035", "H036", "H037", "H038", "H039", "H040", "H041",
           "H042", "H043", "H044", "H045"]
)
# print(f"sikenデータの確認 \n{siken.head()}")  #for debug
print("試験データ")
print(siken)
# 合計点Totalの計算
siken["total"] = siken["Math"] + siken["Eng"] + siken["Jpn"]
print(siken["total"])
# 基本統計量resultの計算
data = siken.describe()
# print(f"試験結果　基本統計量\n{result}")
print(data)
# 偏差値Hensaの計算
siken["hensa"] = (siken["total"]-data.at["mean", "total"]) / data.at["std", "total"]*10 + 50
#print( f"試験結果(偏差値含む)の表示\n{siken}")
print("偏差値\n {} ".format(siken["hensa"]))

# 相関行列r_resultの表示
r = np.corrcoef(siken)
# print(f"相関行列\n{r_result}")
print("相関行列\n r= {}".format(r))
# グラフを作成するためのｘ
x = np.array([np.min(siken["Eng"]),np.max("Eng")])
# 英語と国語グラフ
# 回帰直線の計算と折れ線グラフ
a,b = np.polyfit(siken["Eng"],siken["Jpn"])
# 散布図
plt.title("相関図")
#plt.figure()
# EngとJpnの相関係数は1行2列，MathとJpnの相関係数は1行2列