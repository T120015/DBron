import math
import numpy as np


def main():
    ep = np.array([710, 90])
    check = int(1500)
    # 乗車距離
    ans = 0
    night = 0
    for i in range(1000, 10001, 500):
        kyori = i
        ans = 0
        print(f"距離{kyori}[ｍ]の料金は")
        if kyori <= check:
            ans = ep[0]
        else:
            a = math.ceil((kyori - check)/283)
            ans = ep[1] * round(a) + ep[0]

        print(f"昼間:{ans}円です.")
        night = ans * 1.3
        print(f"夜間:{round(night,-1):.0f}円です.")


main()
