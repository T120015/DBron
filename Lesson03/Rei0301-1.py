#例題9　pnadas csvファイルの読み込み
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

#kimatsu.csvを読み込む，0行目を列の名称（header），0列目を行の名称(index_col)とする
#【入力】

#print(f"試験結果\n{siken}")  #for debug

#合計点を算出
siken["Total"] = siken["Math"]+siken["Eng"]+siken["Jpn"]
mean = np.mean( siken["Total"])
std = np.std( siken["Total"])
siken["Hensa"] = ( siken["Total"] - mean )/std * 10 + 50
#print(f"試験結果\n{siken}")  #for debug

#クラスごとにデータを抽出
#【入力】
siken_b = siken.query("Croom == 'B' ")
siken_c = siken.query("Croom == 'C' ")
#クラスごとに基本統計量を算出
result_a = siken_a.describe()
result_b = siken_b.describe()
result_c = siken_c.describe()
#結果の表示
print(f"Aクラス\n{result_a}")
print(f"Bクラス\n{result_b}")
print(f"Cクラス\n{result_c}")

#合計点平均値のグラフ表示
y = [result_a.at["mean","Total"],result_b.at["mean","Total"],result_c.at["mean","Total"]]
#下記でも同じ
#y = [ np.mean(siken_a["Total"]),np.mean(siken_b["Total"]),np.mean(siken_c["Total"])]
plt.bar(range(3),y,tick_label=["A","B","C"])
plt.title("合計平均点の比較")
plt.xlabel("クラス")
plt.ylabel("合計平均点")
plt.savefig("./img/Rei0301-1.png")