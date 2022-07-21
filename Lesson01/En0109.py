from math import sqrt
import numpy as np

def main():
    student = np.ones((15, 2))
    for i in range(15):
        student[i][0] = np.random.randint(0, 101)
        student[i][1] = np.random.randint(0, 101)
    sum = np.sum(student, axis=1)
    mean = np.mean(sum)
    std = np.std(sum)
    print("偏差値:")
    for i in range(len(sum)):
        print(f"No.{i+1:2}:{(10*(sum[i]-mean)/std)+50:.0f}")


main()
