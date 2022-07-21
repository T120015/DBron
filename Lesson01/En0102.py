import math
import numpy as np


def main():
    num = np.array([5, 6, 8])
    sum = 0
    for i in range(len(num)):
        sum += num[i]
    sum /=2
    ans = sum
    for i in range(3):
        ans *= (sum - num[i])

    print(f"辺の長さが{num[0]},{num[1]},{num[2]},の三角形の面積は,{math.sqrt(ans)}です．")


main()
