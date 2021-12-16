#演習１０
from numpy.lib.type_check import imag
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
#読み込み
weather = pd.read_csv("./data/weather.csv",header=0)

#indexを，Place,Yearとしてpivotテーブル
result = pd.pivot_table(weather, index=["Place","Year"])
#print( f"result\n{result.head()}")   #for debug

#地区ごとのデータ抽出→indexからPlaceの列を取り外す
suwa = result.query("Place =='Suwa'").reset_index("Place",inplace=False)
tokyo = result.query("Place =='Tokyo'").reset_index("Place",inplace=False)
naha = result.query("Place =='Naha'").reset_index("Place",inplace=False)
temp = result.query("Place =='Suwa'")  #for デバッグ 
#print( f"諏訪のデータだけを抽出\n{temp.head()}")   #for debug
print( f"Placeのインデックスを削除 suwa \n{suwa.head()}")  #for debug
#print(f"x軸のデータ \n {suwa.index}")  #for debug
#print(f"y軸のデータ\n{suwa['Temp_mean']}")

#グラフ表示
plt.plot( suwa.index.values, suwa["Temp_mean"],label="Suwa")
plt.plot( tokyo.index.values, tokyo["Temp_mean"],label="Tokyo")
plt.plot( naha.index.values, naha["Temp_mean"],label="Naha")
plt.title("年間平均気温の移り変わり")
plt.xlabel("年")
plt.ylabel("平均気温")
plt.legend()
plt.savefig("./img/En0210-2.png")
