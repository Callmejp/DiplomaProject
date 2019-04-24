import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.preprocessing import image

np.set_printoptions(threshold=np.inf)

classifier = keras.models.load_model('softmax.h5')

# for p in classifier.get_weights():
#     print(p.shape)

"""
Achieve the ouput of the ChestNet in advance
"""
for i in range(0, 19):
    image_path = 'csv/1D_binary/'
    image_path = image_path + str(i) + '.png'
    img = image.load_img(image_path, color_mode="grayscale")
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    predictions = classifier.predict(img)
    print(predictions)

"""
How to write the 'tf' file
"""
# def write4D(handle, arr):
#     i, j, k, l = arr.shape[0], arr.shape[1], arr.shape[2], arr.shape[3]
#     handle.write('[')
#     for q in range(i):
#         handle.write('[')
#         for w in range(j):
#             handle.write('[')
#             for e in range(k):
#                 handle.write('[')
#                 for r in range(l):
#                     handle.write(str(arr[q][w][e][r]))
#                     if r < l - 1:
#                         handle.write(', ')
#                 if e == k - 1:
#                     handle.write(']')
#                 else:
#                     handle.write('], ')     
#             if w == j - 1:
#                 handle.write(']')
#             else:
#                 handle.write('], ')
#         if q == i - 1:
#             handle.write(']')
#         else:
#             handle.write('], ')
#     handle.write(']\n')

# def write2D(handle, arr):
#     k, l = arr.shape[0], arr.shape[1]
#     handle.write('[')
#     for e in range(k):
#         handle.write('[')
#         for r in range(l):
#             handle.write(str(arr[e][r]))
#             if r < l - 1:
#                 handle.write(', ')
#         if e == k - 1:
#             handle.write(']')
#         else:
#             handle.write('], ')        
#     handle.write(']\n')

# def write1D(handle, arr):
#     l = arr.shape[0]
#     handle.write('[')
#     for r in range(l):
#         handle.write(str(arr[r]))
#         if r < l - 1:
#             handle.write(', ') 
#     handle.write(']\n')

# rst = classifier.get_weights()

# with open('chest_1D.tf', 'w') as f:
#     f.write('Conv2D\n')
#     f.write('ReLU, filters=16, kernel_size=[3, 3], input_shape=[64, 64, 1], stride=[1, 1], padding=0\n')
#     write4D(f, rst[0])
#     write1D(f, rst[1])
#     f.write('MaxPooling2D\n')
#     f.write('pool_size=[3, 3], input_shape=[62, 62, 16], stride=[1, 1]\n')

#     f.write('Conv2D\n')
#     f.write('ReLU, filters=32, kernel_size=[1, 1], input_shape=[60, 60, 16], stride=[1, 1], padding=0\n')
#     write4D(f, rst[2])
#     write1D(f, rst[3])
#     f.write('MaxPooling2D\n')
#     f.write('pool_size=[4, 4], input_shape=[60, 60, 32], stride=[2, 2]\n')

#     f.writelines('Conv2D\n')
#     f.writelines('ReLU, filters=64, kernel_size=[3, 3], input_shape=[29, 29, 32], stride=[2, 2], padding=0\n')
#     write4D(f, rst[4])
#     write1D(f, rst[5])
#     f.writelines('MaxPooling2D\n')
#     f.writelines('pool_size=[3, 3], input_shape=[14, 14, 64], stride=[1, 1]\n')

#     f.writelines('ReLU\n')
#     write2D(f, rst[6])
#     write1D(f, rst[7])

#     f.writelines('ReLU\n')
#     write2D(f, rst[8])
#     write1D(f, rst[9])

#     f.writelines('Sigmoid\n')
#     write2D(f, rst[10])
#     write1D(f, rst[11])


