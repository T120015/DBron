import random
import math
import numpy as np


def main():
    ep = np.array([710, 90])
    check = int(1500)
    # 乗車距離
    kyori = random.randrange(1000, 3000, 100)

    print(f"距離{kyori}[ｍ]の料金は")
    if kyori <= check:
        ans = ep[0]
    else:
        a = math.ceil((kyori - check)/283)
        ans = ep[1] * round(a) + ep[0]

    print(f"{ans}円です.")
    ans *= 1.3
    print(f"{round(ans,-1):.0f}円です.")


main()
