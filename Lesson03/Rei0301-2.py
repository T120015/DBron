#例題9　pnadas csvファイルの読み込み
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

#kimatsu.csvを読み込む，0行目を列の名称（header），0列目を行の名称(index_col)とする
siken = pd.read_csv("./data/kimatsu.csv",index_col=0,header=0)

#print(f"試験結果\n{siken}")  #for debug

#合計点を算出
siken["Total"] = siken["Math"]+siken["Eng"]+siken["Jpn"]
mean = np.mean( siken["Total"])
std = np.std( siken["Total"])
siken["Hensa"] = ( siken["Total"] - mean )/std * 10 + 50
#print(f"試験結果\n{siken}")  #for debug

#クラスごとに平均値の計算
#【入力】
print(f"クラスごとの平均値\n{result}")

plt.bar(range(len(result.index)),result["Total"],tick_label=result.index)
plt.title("合計平均点の比較(groupbyメソッド)")
plt.xlabel("クラス")
plt.ylabel("合計平均点")
#plt.legend()
plt.savefig("./img/Rei301-2.png")