import numpy as np
import math

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    list = np.convolve(data_set, weights, mode='valid')
    list = [math.ceil(x) for x in list]
    return list

if __name__ == '__main__':
    data = [1, 2, 3, 6, 9, 12, 20, 28, 30, 25, 22, 20, 15, 12, 10]

    ma = moving_average(np.asarray(data), 5)
    print(ma)

