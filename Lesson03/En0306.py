import pandas as pd
from matplotlib import pyplot as plt
import japanize_matplotlib
from mydblib import my_select as slc



def main():
  data = """
  SELECT answer1, COUNT(answer1) AS cnt
  FROM quest
  GROUP BY answer1
  """

  post_num = slc(data)

  print(post_num)

  #make graph
  plt.bar(post_num["answer1"], post_num["cnt"], tick_label=post_num["answer1"])
  plt.title("アンケート結果")

if __name__ == "__main__":
  main()