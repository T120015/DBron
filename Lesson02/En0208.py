# 演習８　Pandas DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

fig = plt.figure(figsize=(6,8))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
kantou = pd.DataFrame(
    [[879, 2970, 478.4],
     [882, 2008, 308.1],
     [865, 2008, 310.1],
     [956, 7195, 1913.4],
     [953, 6216, 1206.5],
     [1041, 13159, 6168.7],
     [1040, 9048, 3777.7]],
    columns=["h_wage", "population", "p_density"],
    index=["茨城", "栃木", "群馬", "埼玉", "千葉", "東京", "神奈川"]
)

# for debug
print(f"kantou\n{kantou}")

# 基本統計量の表示
resutlt = kantou.describe()
print("基本統計量:\n{}".format(resutlt))
# 最低時給の棒グラフの表示
ax1.bar(range(len(kantou["h_wage"])),
        kantou["p_density"], tick_label=kantou.index)
ax1.set_title("関東地方の最低賃金ヒストグラム")
ax1.set_xlabel("都道府県名")
ax1.set_ylabel("最低時給")
#plt.savefig("./img/En0208-1.png")
# 人口と人口密度の列をnumpy.arrayに変換
population = np.array(kantou["population"])
p_density = np.array(kantou["p_density"])
# print(population)   #for debug

# 相関係数 相関行列の0行1列目
r = np.corrcoef(population, p_density)[0, 1]

# 回帰直線の計算
a, b = np.polyfit(population, p_density, 1)

# 回帰直線入りの散布図作成
x = np.array([np.min(population), np.max(population)])
y = a * x + b
ax2.plot(x,y,color = "red", label = "y = {}x +{}".format(a,b))
ax2.scatter(population, p_density)
ax2.set_title("関東地方の人口と人口密度: r={}".format(r))
ax2.set_xlabel("人口")
ax2.set_ylabel("人口密度")
# 散布図の点にラベルの追加
for i, label in enumerate(kantou.index):
    ax2.annotate(label, (population[i], p_density[i]))
ax2.legend()
#plt.savefig("./img/En0208-2.png")
fig.tight_layout()
plt.savefig("./img/En0208.png")