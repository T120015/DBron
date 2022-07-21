import pandas as pd
from scipy.stats import ttest_rel as tt
from mydblib2 import my_select as slc

sqlstr = f"""
SELECT *
FROM weather
WHERE YEAR = 2019
;
"""
weather = slc("webprog", sqlstr)

#平均
result = weather.groupby("Area").mean()
#平均 出力
print(
    f"それぞれ平均:\n東京-{result['Temp_mean']['Tokyo']}, 大阪-{result['Temp_mean']['Osaka']}\n")
#t検定
g_tokyo = weather.query("Area == 'Tokyo'")['Temp_mean']
g_osaka = weather.query("Area == 'Osaka'")['Temp_mean']
t_val, p_val = tt(g_tokyo, g_osaka)
#t検定 出力
print(f"ttest p_val= {p_val}")
