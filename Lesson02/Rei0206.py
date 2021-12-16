# 例題６　基本統計量の計算
import pandas as pd

# Seriesメソッドで1次元配列を意味する
Math = pd.Series([50, 80, 65, 55, 50], index=[
                 "H001", "H002", "H003", "H004", "H005"])
Eng = pd.Series([60, 60, 75, 70, 45], index=[
                "H001", "H002", "H003", "H004", "H005"])

# 合計点を表示する
Total = Math + Eng
print(f"合計点\n{Total}")
# Totalのデータ型を確認する
print(f"Totalのデータ型は {type(Total)} ")
# 基本統計量をresultに保存する
result = Total.describe()
print(f"基本統計量 \n{result['std']}")
# 平均値のみ参照する場合
# myu = 【入力】
#print(f"平均値は {myu}")
# 上記2行を1行で記述すると "(ダブルコート）と'(シングルコート)の使い分け
# print(f"標準偏差は{【入力】}")
