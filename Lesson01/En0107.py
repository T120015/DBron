import numpy as np


def main():
    a = np.array([0, 1])
    for i in range(2,11):
        a = np.append(a, (a[i-1]+a[i-2]))
    print(a)


main()
