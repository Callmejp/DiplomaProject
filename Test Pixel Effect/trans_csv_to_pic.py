import csv
import numpy as np
from matplotlib import pyplot as plt

"""
You can run the code to transform the line of 
a csv file to the original picture to show
"""

filename = 'mnist_test.csv'

with open(filename) as f:
    tests = csv.reader(f, delimiter=',')

    for test in tests:
        image = np.reshape(np.float64(test[1:len(test)]), [28, 28])
        fig = plt.figure()

        ax1 = fig.add_subplot(221)
        ax1.imshow(image, cmap="gray_r")

        ax2 = fig.add_subplot(222)
        ax2.imshow(image, cmap="gray")

        lighter = np.clip(image + 0.5 * 256, 0.0, 255.0)
        ax3 = fig.add_subplot(223)
        ax3.imshow(lighter, cmap="gray")

        darker = np.clip(image - 0.5 * 256, 0.0, 255.0)
        ax3 = fig.add_subplot(224)
        ax3.imshow(darker, cmap="gray")
        plt.show()
        break

