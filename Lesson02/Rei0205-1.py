#例題0205－1　Pandasモジュール1次元配列 Series
import pandas as pd

#Seriesメソッドで1次元配列を意味する
Math = pd.Series([50,80,65,55,50])
Eng = pd.Series([60,60,75,70,45])

#合計点を表示する
Total = Math + Eng
print( Math )
print( Eng )
print( Total )
#Totalのデータ型を確認する
print( type(Total) )