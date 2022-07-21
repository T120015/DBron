#演習９　
import pandas as pd
import matplotlib.pyplot as plt
#csvファイルからデータの読み込み
#【入力】
df: pd.DataFrame = pd.read_csv()

#kinds列の値ごとに平均値を算出する
#【入力】
#print(f"result\n{result}")  #for debug

#resultの転置行列をresult_transとする,
#【考察2の入力】
#print(f"result_transpose\n{result_trans}")  #for debug
result_trans = df
#部位ごとに棒グラフを作る
for col in result_trans.columns:
    plt.plot(result_trans.index,result_trans[col],label=col)
plt.title("iris mean")
plt.xlabel("parts")
plt.ylabel("mm")
plt.legend()
plt.savefig("./img/En0301-2.png")
