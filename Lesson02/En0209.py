#演習９　
import pandas as pd
import matplotlib.pyplot as plt

iris = pd.read_csv("./data/iris.csv",header=0)

#kinds列の値ごとに平均値を算出する
result = iris.groupby("kinds").mean()
print(f"result\n{result}")

#部位ごとに棒グラフを作る
for i,col in enumerate(result.columns):
    plt.plot(result.index,result[col],label=col)
plt.title("iris mean")
plt.xlabel("kinds")
plt.ylabel("mm")
plt.legend()
plt.savefig("./img/En0209.png")