# 例題0401-1 　2つの平均値の検定
# テーブルsiken1には，下記データが格納されている
#   cram　　english/none　　英語塾に行っている/行っていない
#   club    none/baseball/brassband  帰宅部/野球部/ブラスバンド部
#   score   英語の試験結果
# t検定で，英語の塾に行っているグループと，行っていないグループに平均点の差があるか検定する

from scipy.stats import ttest_ind as tt
from scipy.stats import bartlett as bt
import pandas as pd
from mydblib2 import my_select

# SQLの設定
# tableに検索するtable名
sqlstring = f"""
SELECT *
FROM siken1
;
"""
# webprogデータベースのsiken1テーブルのレコードを読み込み
siken = my_select("webprog", sqlstring)
# cramごとの平均値
result = siken.groupby("cram").mean()
# それぞれの平均値を表示
# 【入力】SELECT *
print(f"平均値：{result['score']}")


# 英語塾に行っている人と，行っていない人の平均値に差があるか
g_eng = siken.query("cram == 'english'")['score']
g_none = siken.query("cram == 'none'")['score']
# print(f"g_eng \n{g_eng}") #for debug

# 手順(1)分散は等しいと仮定して良いかの検定
# b_val(検定値)，p_val(p値：有意水準　0.05未満なら分散が等しくない)
b_val, p_val = bt(g_eng, g_none)

#print( f"bartlett p_value={p_val}")

# 手順(2)分散に応じてt検定により二つの集団の平均値に差があるか検定する
# t検定は，scipy.statsモジュールのttest_indメソッドを使う
# 平均値の検定 分散の検定により検定の種類が分かれる
if(p_val >= 0.05):
    # 分散が等しい(p_val>=0.05)のときstudentのt検定(equal_var=True)
    t_val, p_val = tt(g_eng, g_none, equal_var=True)
else:
    # 分散が等しくない(p_val<0.05)のときweltchのt検定(equal_var=False)
    t_val, p_val = tt(g_eng, g_none, equal_var=False)
print(f"ttestの結果 p_value={p_val} ")

# t検定をした結果，p_val>=0.05なら平均値に差がない，p_val<0.05なら平均値に差がある
