#例題2　Rei0202.py
import numpy as np
import matplotlib.pyplot as plt

#関数の定義
def sig(x):
    y = 1 / ( 1 + np.exp(-x) ) 
    return y 

def tanh(x):
    y = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x) )
    return y

def ReLU(x):
    y = np.array([])
    for v in x:
        if ( v <= 0 ):
            y = np.append(y , 0) 
        else:
            y = np.append(y , v) 
        
    return y


#from matplotlib import pyplot as plt #importの別な書式  上の行と同じ結果

#ｘとｙの値をセットする
x = np.arange(-2, 2, 0.05)   #-3以上3未満を0.5刻みで
y1 = sig(x)       #リストxに対応したsin(x)のリストがyとなる
y2 = tanh(x)
y3 = ReLU(x)

#print( f"x={x}" )   #for debug

plt.title("Activation function")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x, y1,label="Sigmoid")
plt.plot(x, y2,label="tanh")
plt.plot(x, y3,label="ReLU")
plt.legend()   #plotのlabelを表示する
#plt.show()  #インライン表示可能な開発環境の時
plt.savefig("./img/En0202.png")
