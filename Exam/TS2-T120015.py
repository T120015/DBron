import pandas as pd
from scipy.stats import f_oneway as fone
from mydblib2 import my_select as slc
from tukey import tukey_hsd as tukey

print("T120015 小問0")
# SQLからのdata取得
sqlstr = f"""
SELECT *
FROM siken
;
"""
data = slc("wptest", sqlstr)
# data平均
result = data.groupby("Croom").mean().iloc[:, 1:4]
# 出力
print(result)
# 検定
g_A = data.query("Croom == 'A'")['Math']
g_B = data.query("Croom == 'B'")['Math']
g_C = data.query("Croom == 'C'")['Math']
# 出力
f_val, p_val = fone(g_A, g_B, g_C)
print(f"Mathについての一元配置分散分析:\nf_val = {f_val:.3f}, p_val = {p_val:.3f}\n")
tukey(["A", "B", "C"], g_A, g_B, g_C)
