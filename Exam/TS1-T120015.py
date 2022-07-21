import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from mydblib2 import my_select as select

print("T120015 小問3")

sql = f"""
    SELECT *
    FROM iris
    ;
    """


iris = select('wptest', sql)
pl = iris["petallength"]
pw = iris["petalwidth"]
r = np.corrcoef(pl, pw)[0, 1]
print(f"相関係数:{r}")
# 回帰直線の計算
p, q = np.polyfit(pl, pw, 1)
# 回帰直線のための座標計算
x = np.linspace(np.min(pl), np.max(pl))
y = p * x + q


# 散布図
plt.scatter(pl, pw)
# 回帰直線
plt.plot(x, y, label="y={:.3f}x+{:.3f}".format(p, q), color="red")
# ラベル
plt.title(f"TP1: 相関係数:{r:.3f}")
plt.xlabel("perallength")
plt.ylabel("petalwiedth")
plt.legend()
plt.savefig(f"./TS1-T120015.png")
plt.close()
