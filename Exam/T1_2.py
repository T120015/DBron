import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from mydblib2 import my_select as select

sql = f"""
    SELECT *
    FROM iris
    ;
    """

iris = select('wptest', sql)
mean = iris.groupby("kinds").mean()
std = iris.groupby("kinds").std()

list = iris.columns.values


print("平均:\n{}\n標準編差:\n{}".format(mean, std))

#グラフ

