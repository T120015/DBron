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
data = iris.describe().iloc[:,1:]


list = iris.columns.values
print(list)

mean = data.iloc[2,1:]
std = data.iloc[3,1:]


#df = pd.DataFrame({"mean": [mean[list[1]]], "std": [std[list[1]]]})

print(mean)
# print("平均:{}\n標準編差:{}".format())
