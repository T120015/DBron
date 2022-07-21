#例題2　Rei0202.py
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt #importの別な書式  上の行と同じ結果

#ｘとｙの値をセットする
x = np.arange(-np.pi,np.pi,0.1)   #-3以上3未満を0.5刻みで
y = np.sin(x)       #リストxに対応したsin(x)のリストがyとなる

#print( f"x={x}" )   #for debug
#print( f"y={y}" )   #for debug

#折れ線グラフ
plt.plot(x,y)
plt.title("y=sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()  #plotのlabelを表示する
#plt.show()  #インライン表示可能な開発環境の時
plt.savefig("./img/Rei0202.png")

#考察
# (1) もう少し滑らかに
# (2) -πからπの範囲で