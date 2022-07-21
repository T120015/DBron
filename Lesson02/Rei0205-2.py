#例題0205－2　Pandasモジュール1次元配列 Seriesにindexを付加
import pandas as pd

#Seriesメソッドで1次元配列を意味する
Math = pd.Series([50,80,65,55,50],index=["H001","H002","H003","H004","H005"])
Eng = pd.Series([60,60,75,70,45],index=["H001","H002","H003","H004","H005"])

#合計点を表示する
Total = Math + Eng
print( Total )
#Totalのデータ型を確認する
print( type(Total) )
#indexのみ参照する
print( Total.index )
