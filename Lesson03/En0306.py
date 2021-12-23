import pandas as pd
from matplotlib import pyplot as plt
from mydblib import my_select as slc



def main():
  data = """
  SELECT answer1, COUNT(answer1) AS cnt
  FROM quest
  """

  pos_num = slc(data)

  print(pos_num)

if __name__ == "__main__":
  main()