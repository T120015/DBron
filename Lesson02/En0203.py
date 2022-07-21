# 例題３
import numpy as np
import matplotlib.pyplot as plt

# 最低賃金と人口密度
h_wage = np.array([879, 882, 865, 956, 953, 1041,
                  1040, 859, 877, 861, 858, 866, 877])
p_density = np.array([478.4, 308.1, 310.1, 1913.4, 1206.5,
                     6168.7, 3777.7, 183.1, 251, 275.7, 187.7, 187, 154.8])
# print( f"身長 {sintyou}")    #for debug
# print( f"体重 {taijyuu}")    #for debug

# 相関行列(Correlation Matrix) cm を求める
cm = np.corrcoef(h_wage,p_density)
print(f"相関行列\n{cm}")
# 相関行列の0行1列から相関係数をｒを代入
r = cm[0,1]

# 回帰直線の傾きaと切片ｂを計算
a,b = np.polyfit(h_wage,p_density,1)
# 回帰直線の方程式を表示
print("回帰直線の方程式: y={}x+{}".format(a,b))
# 回帰直線の座標データを作成
# xの値は，x軸の最小値と最大値
x = np.linspace(np.min(h_wage),np.max(h_wage),20)
# ｙの値は，回帰直線に合わせて算出
y = a * x + b
print("x={}\ny={}".format(x,y))

# グラフタイトルに相関係数を表示する
plt.title("Scatter r={}".format(r))
# x軸とy軸のラベルを設定する
plt.xlabel("height")
plt.ylabel("weight")
# 散布図のパラメータを設定する
plt.scatter(h_wage,p_density, color="red")
# 回帰直線のグラフ表示
plt.plot(x,y,label="y={}x+{}".format(a,b))
# h凡例グラフ表示/出力
# plt.show()
plt.legend()
plt.savefig("./img/En0203.png")
