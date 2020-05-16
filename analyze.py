from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import json

algorithms = [
    'Sasha1',
    'Sasha2',
    'Misha1',
]

for algo in algorithms:
    with open(algo + ".txt", "r") as file:
        data = json.loads(file.read())
        lists = data['time'].items()
        x_raw, y_raw = zip(*lists)

        x = [int(i) for i in x_raw]
        y = [float(i) for i in y_raw]

        coefs = np.polyfit(x, y, 2)
        predict = np.poly1d(coefs)

        x_test = np.linspace(0, 1000)
        y_predict = predict(x_test[:, None])

        plt.subplot(211)
        plt.tight_layout()
        plt.scatter(x, y, alpha=0.5, s=8)
        plt.title('Bench time, ' + algo)
        plt.xlabel('maze size')
        plt.ylabel('time, s')
        plt.plot(x_test, y_predict, 'r')

        plt.subplot(212)
        plt.tight_layout()
        lists = data['path'].items()
        x_raw, y_raw = zip(*lists)
        x = [int(i) for i in x_raw]
        y = [int(i) for i in y_raw]

        coefs = np.polyfit(x, y, 2)
        predict = np.poly1d(coefs)

        x_test = np.linspace(0, 1000)
        y_predict = predict(x_test[:, None])

        plt.title('Path size, ' + algo)
        plt.xlabel('maze size')
        plt.ylabel('path size')
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 1))
        plt.scatter(x, y, alpha=0.5, s=8, c='g')
        plt.plot(x_test, y_predict, 'r')
        plt.tight_layout()

        plt.show()
