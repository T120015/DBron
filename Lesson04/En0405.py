import pandas as pd
from scipy.stats import f_oneway as fone
from mydblib2 import my_select as slc

sqlstr = f"""
SELECT *
FROM weather
WHERE YEAR BETWEEN 2010 AND 2019
;
"""
weather = slc("webprog", sqlstr)
result = weather.groupby('Area').mean()

print("地区ごとの平均気温:\n{}".format(result))

g_fukuoka = weather.query("Area == 'Fukuoka'")['Temp_mean']
g_osaka = weather.query("Area == 'Osaka'")['Temp_mean']
g_nagoya = weather.query("Area == 'Nagoya'")['Temp_mean']

b_val, p_val = fone(g_fukuoka, g_osaka, g_nagoya)
print(f"一元配置分散分析 p_val= {p_val:.3f}")
