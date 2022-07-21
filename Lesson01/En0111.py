import numpy as np
import matplotlib.pyplot as plt


def main():
    fig = plt.figure()
    sai = np.array([0, 0])
    base = np.array([])
    for i in range(300):
        sai[0] = np.random.randint(1, 7)
        sai[1] = np.random.randint(1, 7)
        sum = sai[0]+sai[1]
        base = np.append(base, sum)
    mean = np.mean(base)
    std = np.std(base)
    data, hist = np.histogram(base, range=(2, 12))

    print(f"平均:{mean}\n標準偏差:{std}\n度数分布:{data}\n")
    plt.step(hist[:-1], data, where='post')
    fig.savefig("img.png")


if __name__ == "__main__":
    main()
