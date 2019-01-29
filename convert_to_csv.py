import numpy as np
import Image
import csv
from transform import number_of_0


with open('flower.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for pid in range(1, 11):
        length = number_of_0(pid)
        s0 = ""
        for j in range(length):
            s0 += "0"
        image_name = 'image_' + s0 + str(pid) + '.jpg'
        image_path = 'flowers/' + image_name
        im = Image.open(image_path)
        im = np.array(im)
        # print(im)
        image_array = [0]
        for i in range(64):
            for j in range(64):
                for k in range(3):
                    image_array.append(im[i][j][k])

        # print(image_array)

        writer.writerow(image_array)
