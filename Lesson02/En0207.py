#演習７最低時給
import numpy as np
from numpy.core.fromnumeric import mean, std
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

#pandas Seriesで都道府県別最低賃金データ
h_wage=pd.Series(
    [889,822,821,853,822,822,828,879,882,865,956,953,1041,1040,
    859,877,861,858,866,877,880,913,955,902,896,937,992,928,866,859,
    821,824,862,899,857,824,848,821,820,870,821,821,821,822,821,821,820],
    index=['北海道','青 森','岩 手','宮 城','秋 田','山 形','福 島','茨 城',
    '栃 木','群 馬','埼 玉','千 葉','東 京','神奈川','新 潟','富 山','石 川',
    '福 井','山 梨','長 野','岐 阜','静 岡','愛 知','三 重','滋 賀','京 都',
    '大 阪','兵 庫','奈 良','和歌山','鳥 取','島 根','岡 山','広 島','山 口',
    '徳 島','香 川','愛 媛','高 知','福 岡','佐 賀','長 崎','熊 本','大 分',
    '宮 崎','鹿児島','沖 縄']
)

#基本統計量
result = h_wage.describe()

#pandasヒストグラム算出
plt.hist(h_wage, bins=20)
plt.title("都道府県別最低賃金ヒストグラム")
plt.xlabel("最低賃金")
plt.ylabel("度数")
plt.savefig("./img/En0207.png")
