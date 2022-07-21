#例題３
import numpy as np
import matplotlib.pyplot as plt

#身長と体重のベクトルデータを正規乱数で作成
sintyou = np.array( np.random.normal(160,15,30) )
taijyuu = np.array( np.random.normal(57,10,30) )
#print( f"身長 {sintyou}")    #for debug
#print( f"体重 {taijyuu}")    #for debug

#相関行列(Correlation Matrix) cm を求める
#【入力】
#print(f"相関行列 \n {cm}")
#相関行列の0行1列から相関係数ｒを代入
#【入力】

#回帰直線の傾きaと切片ｂを計算
#【入力】
#回帰直線の方程式を表示
#print(f"回帰直線の方程式は y = {a}x + {b}")
#回帰直線の座標データを作成
#xの値は，x軸の最小値と最大値
#【入力】
#ｙの値は，回帰直線に合わせて算出
#y = a * x + b
#print(f"x = {x}")  #for debug
#print(f"y = {y}") #for debug

#グラフタイトルに相関係数を表示する
#plt.title(f"Scatter r={r}")
#x軸とy軸のラベルを設定する
plt.xlabel("height" )
plt.ylabel("weight" )
#散布図のパラメータを設定する
#plt.scatter(x, y)
#回帰直線のグラフ表示
#plt.plot(x,y,label=f"y={a}x+{b}")
#凡例とグラフ表示/出力
#plt.show()
plt.legend()
plt.savefig("./img/Rei0203.png")
