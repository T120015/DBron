#例題８ pandas DataFrame
import pandas as pd
#pandas DataFrameで2次元配列の定義
#columnsは，カラム（列）名
#indexは，行の名前
siken = pd.DataFrame(
    [ [50 , 60, 70],
      [80 , 60, 55],
      [65 , 75, 50],
      [55 , 70, 60],
      [50 , 45, 60]  ],
    columns = ["suugaku","kokugo","eigo"] , 
    index = ["H001","H002","H003","H004","H005"]
)
#合計点を計算
siken["total"] = siken["suugaku"]+siken["kokugo"]+siken["eigo"]
#sikenの表示
print(f"siken\n{siken}")
#カラム名のみ表示
print(f"カラム名{siken.columns}")
#数学の点数のみ表示
print(f"数学の点数 \n{siken['suugaku']}")
#行の名前のみ表示
print(f"行の名前{siken.index}")
#H001のデータを表示 locメソッド
print(f"H001のデータ\n{siken.loc['H001']}")
#2行目のデータを表示　ilocメソッド
print(f"2行目のデータを表示\n{siken.iloc[2]}")
#H003の数学suugakuのデータを表示　atメソッド
print(f"H003の合zz計点totalのデータを表示{siken.at['H003','suugaku']}")

