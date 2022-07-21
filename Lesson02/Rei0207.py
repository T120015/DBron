#例題７　標準正規乱数のヒストグラム
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#標準正規乱数を作成する
s_normal = pd.Series( np.random.randn(10000))
#確認のために基本統計量
print( f"基本統計量 \n{s_normal.describe()}")

#ヒストグラム表示
plt.hist(s_normal, bins=20 )
plt.title("Standard normal distribution")
plt.xlabel("x")
plt.ylabel("N")
plt.savefig("./img/Rei0207.png")


