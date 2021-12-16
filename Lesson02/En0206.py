# 演習５
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

# 最低時給
h_wage = np.array([
    889, 822, 821, 853, 822, 822, 828, 879, 882, 865, 956, 953, 1041, 1040,
    859, 877, 861, 858, 866, 877, 880, 913, 955, 902, 896, 937, 992, 928, 866, 859,
    821, 824, 862, 899, 857, 824, 848, 821, 820, 870, 821, 821, 821, 822, 821, 821, 820
])

# 基本統計量
print(f"時給平均 {np.mean(h_wage)}")
print(f"時給標準偏差 {np.std(h_wage)}")
print(f"時給  0％ {np.min(h_wage)}")
print(f"時給 25％ {np.percentile(h_wage,q=25)}")
print(f"時給 50％ {np.median(h_wage)}")
print(f"時給 75％ {np.percentile(h_wage,q=75)}")
print(f"時給100％ {np.max(h_wage)}")
# 度数分布
hst, border = np.histogram(
    h_wage, bins=10, range=(np.min(h_wage), np.max(h_wage)))
hst = np.append(hst,0)
# 棒グラフ表示
plt.bar(border, hst, tick_label=border)
# x軸目盛ラベルのフォントサイズを変更する
plt.xticks(fontsize=6)
plt.title("最低時給ヒストグラム")
plt.xlabel("賃金")
plt.ylabel("度数")
plt.savefig("./img/En0206.png")
