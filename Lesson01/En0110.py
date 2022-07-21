import numpy as np


def main():
    sai = np.array([0, 0, 0])
    data = np.array([])
    for i in range(100, 1001, 100):
        for k in range(i):
            sum = 0
            for j in range(3):
                sai[j] = np.random.randint(1, 7)
                sum += sai[j]
            data = np.append(data,sum) 
        print(f"試行回数:{i}回\nMean:{np.mean(data)}, Std:{np.std(data)}")


main()
