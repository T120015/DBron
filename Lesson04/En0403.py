import pandas as pd
from scipy.stats import ttest_rel as tt, bartlett as bt
from mydblib2 import my_select as slc

sqlstr = f"""
SELECT *
FROM weather
WHERE YEAR = 2019
;
"""

weather = slc("webprog", sqlstr)
result = weather.groupby("Area").mean()

print(
    f"それぞれ平均:\n東京-{result['Temp_mean']['Tokyo']}, 大阪-{result['Temp_mean']['Osaka']}\n")

g_tokyo = weather.query("Area == 'Tokyo'")['Temp_mean']
g_osaka = weather.query("Area == 'Osaka'")['Temp_mean']

b_val, p_val = bt(g_tokyo, g_osaka)

if(p_val >= 0.05):
    t_val, p_val = tt(g_tokyo, g_osaka, equal_var=True)
else:
    t_val, p_val = tt(g_tokyo, g_osaka, equal_var=False)

print(f"ttest p_val= {p_val}")
