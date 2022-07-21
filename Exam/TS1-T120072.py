#問題1 小問0
print("T120072 小問番号0\n")
import numpy as np
import matplotlib.pyplot as plt

from mydblib2 import my_select
import pandas as pd

#SQLの設定  
sqlstring =  f"""
    SELECT *
    FROM iris
    ;
"""
#wptestデータベースのirisテーブルのレコードを読み込み
iris = my_select( "wptest",sqlstring ).drop('iris_id', axis=1).drop('kinds', axis=1)

sepallength = iris["sepallength"]
sepalwidth = iris["sepalwidth"]
petallength = iris["petallength"]
petalwidth = iris["petalwidth"]
#print( f"sepallength\n {sepallength}")    #for debug
#print( f"sepalwidth\n {sepalwidth}")    #for debug
#print( f"petallength\n {petallength}")    #for debug
#print( f"petalwidth\n {petalwidth}")    #for debug

#相関行列
print("相関行列\n")
matrix = np.corrcoef(iris, rowvar=False)
print(matrix)

#相関行列の0行1列から相関係数をｒを代入
r_matrix = np.corrcoef(sepallength, sepalwidth)
r = r_matrix[0,1]
#グラフタイトルを表示する
plt.title(f"r={r:.3f}")
#x軸とy軸のラベルを設定する
plt.xlabel("sepallength")
plt.ylabel("sepalwidth")
#散布図のパラメータを設定する
plt.scatter(sepallength,sepalwidth)
#h凡例グラフ表示/出力
plt.show()
plt.savefig("./TS1-T120072.png")
