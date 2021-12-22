#例題２　seabornモジュールpairplot図
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

#csvファイル読み込み
siken = pd.read_csv("./data/kimatsu.csv",header=0)

#pairplot図作成
#【入力】
#クラスごとに色分け
#sns.pairplot(siken, hue="Croom")
plt.savefig("./img/Rei0302.png")
