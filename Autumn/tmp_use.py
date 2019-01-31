import csv
import Image
import numpy as np


with open('autumn.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for pid in range(1, 17):
        image_name = str(pid) + '.jpg'
        image_path = 'tmp_right_save/' + image_name
        im = Image.open(image_path)
        im = np.array(im)
        # print(im.shape)
        image_array = [0]
        for i in range(66):
            for j in range(200):
                for k in range(3):
                    image_array.append(im[i][j][k])
        # print(image_array)
        writer.writerow(image_array)
