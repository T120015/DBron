import pandas as pd
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def tukey_hsd(ind, *args):

    data_arr = np.hstack(args)
    ind_arr = np.array([])
    for x in range(len(args)):
        ind_arr = np.append(ind_arr, np.repeat(ind[x], len(args[x])))
    return pairwise_tukeyhsd(data_arr, ind_arr)  # print -> return に変更
