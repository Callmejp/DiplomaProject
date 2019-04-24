import csv
from PIL import Image
import numpy as np


with open('chest_1D.csv', 'w', newline='') as f:

    writer = csv.writer(f, delimiter=',')

    for pid in range(19):
        image_name = str(pid) + '.png'
        image_path = 'csv/1D_binary/' + image_name

        im = Image.open(image_path)
        im = np.array(im)
        print(im.shape)
        image_array = [0]

        for i in range(64):
            for j in range(64):
                    image_array.append(im[i][j])

        writer.writerow(image_array)