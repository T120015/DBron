#例題1　モジュールのインポートとメソッドの利用
import random

#0以上1未満の一様乱数
print( f"一様乱数　{random.random()}")

#0,100，200，…，900のいずれか
print( f"範囲を指定した乱数 {random.randrange(0,1000,100)}")

#1以上6以下のいずれか
print( f"整数の乱数 {random.randint(1,6)}")
