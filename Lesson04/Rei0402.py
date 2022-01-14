# 例題0402 　3つ以上の母集団の平均値の検定
# テーブルsiken1には，下記データが格納されている
#   club    none/baseball/brassband  帰宅部/野球部/ブラスバンド部
#   score   英語の試験結果
# 分散分析で，所属する部活により平均点の差があるか検定する

############# Tukey_Cramerの多重分析モジュール ########
# ind: Group index
# *args: data
import pandas as pd
from scipy.stats import f_oneway as fone
from mydblib2 import my_select


def tukey_hsd(ind, *args):
    import pandas as pd
    import numpy as np
    from statsmodels.stats.multicomp import pairwise_tukeyhsd

    data_arr = np.hstack(args)
    ind_arr = np.array([])
    for x in range(len(args)):
        ind_arr = np.append(ind_arr, np.repeat(ind[x], len(args[x])))
    print(pairwise_tukeyhsd(data_arr, ind_arr))


if __name__ == "__main__":
    # SQLの設定
    # tableに検索するtable名
    sqlstring = f"""
    SELECT *
    FROM siken1
    ;
    """
    # webprogデータベースのsiken1テーブルのレコードを読み込み
    siken = my_select("webprog", sqlstring)
    print(siken)
    # クラブ活動別に平均値の表示
    result = siken.groupby("club").mean()
    print("平均:{}\n".format(result))

    # cram(塾)がenglishとnoneを抽出　score列のみ
    g_none = siken.query("club == 'none'")['score']
    g_baseball = siken.query("club == 'baseball'")['score']
    g_brassband = siken.query("club == 'brassband'")['score']

    print(g_none)

    # 手順(1)3つ以上の母集団の平均値の検定は，1元配置分散分析 f_oneway を行う
    # b_val(検定値)，p_val(p値：有意水準　0.05未満なら分散が等しくない)
    b_val, p_val = fone(g_none, g_baseball, g_brassband)
    print(f"一元配置分散分析 p_value={p_val:.3f}")

    # 手順(2)有意差があるときp_val < 0.05 のとき，多重比較をする
    # 多重比較は，tukey_hsd メソッドを使う
    # 平均値の検定 分散の検定により検定の種類が分かれる
    if(p_val < 0.05):
        tukey_hsd(["none", "baseball", "blassband"],
                  g_none, g_baseball, g_brassband)

        # 多重比較をした結果，reject(仮説の棄却)がTrueの組み合わせは有意差あり
