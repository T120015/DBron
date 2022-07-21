#例題2　Rei0202.py
import numpy as np
import matplotlib.pyplot as plt

#from matplotlib import pyplot as plt #importの別な書式  上の行と同じ結果

#ｘとｙの値をセットする
x = np.arange(-5, 5, 0.05)   #-3以上3未満を0.5刻みで
y = 1 / ( 1 + np.exp(-x) )      
y1 = (1 / ( 1 + np.exp(-x) ))*(1-(1 / ( 1 + np.exp(-x) )))

#print( f"x={x}" )   #for debug
#print( f"y={y}" )   #for debug

plt.title("Sigmoid")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x, y,label="f(x)")
plt.plot(x,y1,label="f(x)(1-f(x))")
plt.legend()   #plotのlabelを表示する
#plt.show()  #インライン表示可能な開発環境の時
plt.savefig("./img/En0201.png")
