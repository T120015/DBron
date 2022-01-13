import imp
import pandas as pd
from mydblib2 import my_select as slc
from scipy.stats import ttest_ind as tt, bartlett as bt

"""
SQLの設定
"""
sqlstr = f"""
SELECT *
FROM siken2
;
"""
#dataの抽出
siken = slc("webprog", sqlstr)
j_avg = siken["Jpn"].mean()
m_avg = siken["Math"].mean()
#平均
print(f"数学平均：{m_avg}\n国語平均：{j_avg}")
#f検定
b_val, p_val = bt(m_avg,j_avg)
print(f"Bartlett p_val= {p_val}")

#t検定
if (p_val >=0.05):
    t_val, p_val = tt(m_avg, j_avg,equal_var=True)
else:
    t_val, p_val = tt(m_avg, j_avg,equal_var=False)

print(f"ttes p_val= {p_val}")
