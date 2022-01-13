import pandas as pd
from scipy.stats import ttest_ind as tt, bartlett as bt
from mydblib2 import my_select as slc

sqlstr = f"""
SELECT *
FROM weather
WHERE YEAR = 2019
;
"""

weather = slc("webprog", sqlstr)
result = weather.groupby("Area").mean()

print(f"{result}")