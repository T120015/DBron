#例題８
import numpy as np

#サイコロを100回投げた結果をsaikoroに代入する
saikoro = np.random.randint(1,6,100)
print(saikoro) #for debug

avg = np.mean( saikoro )
st = np.std( saikoro )
print(f"平均={avg}  標準偏差={st}")