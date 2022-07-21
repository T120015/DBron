#演習１０
from numpy.lib.type_check import imag
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

#weatherには，idnexのカラムは付加されていない
weather = pd.read_csv("./data/weather.csv",header=0)

#地区ごとのデータ抽出 indexのカラムは付加されていない
suwa = weather.query( "Place == 'Suwa'")
tokyo = weather.query( "Place == 'Tokyo'")
naha = weather.query( "Place == 'Naha'")

#年度ごとの平均値 indexはYearとなる
suwa_mean = suwa.groupby("Year").mean()
tokyo_mean = tokyo.groupby("Year").mean()
naha_mean = naha.groupby("Year").mean()
print(suwa_mean.head()) #for debug
#print(suwa_mean.index) #for debug

#グラフ表示
plt.plot( suwa_mean.index.values,suwa_mean["Temp_mean"],label="Suwa")
plt.plot( tokyo_mean.index.values,tokyo_mean["Temp_mean"],label="Tokyo")
plt.plot( naha_mean.index.values,naha_mean["Temp_mean"],label="Naha")
plt.title("年間平均気温の移り変わり")
plt.xlabel("年")
plt.ylabel("平均気温")
plt.legend()
plt.savefig("./img/En0210-1.png")