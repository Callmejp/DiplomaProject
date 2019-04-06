import sys
sys.path.insert(0, '../ELINA/python_interface/')
import os
from eran import ERAN
from read_net_file import *
import tensorflow as tf
import csv
import time
import argparse


def normalize(image, dimension, num_pixels, means, stds):
    if dimension == 1:
        for i in range(len(image)):
            image[i] = (image[i] - means[0])/stds[0]
    else:
        count = 0
        tmp = np.zeros(num_pixels)
        length = int(num_pixels / dimension)
        for i in range(length):
            tmp[count] = (image[count] - means[0])/stds[0]
            count = count + 1
            tmp[count] = (image[count] - means[1])/stds[1]
            count = count + 1
            tmp[count] = (image[count] - means[2])/stds[2]
            count = count + 1

        if is_conv:
            for i in range(num_pixels):
                image[i] = tmp[i]
        else:
            count = 0
            for i in range(length):
                image[i] = tmp[count]
                count = count+1
                image[i+length] = tmp[count]
                count = count+1
                image[i+length*2] = tmp[count]
                count = count+1


parser = argparse.ArgumentParser(description="test the network by Deeppoly")
parser.add_argument("network", type=str, help="the path of the network you want to test")
parser.add_argument("epsilon", type=float, help="perturbation to the input image")
parser.add_argument("dataname", type=str, help="the path of the dataset you use")
parser.add_argument("-domain", type=str, choices=["deeppoly", "deepzono"], default="deeppoly",
                    help="choose the abstract domain")
parser.add_argument("-normalize", type=float, default=0, help="extra normalization")
parser.add_argument("-dimension", type=int, choices=[1, 3], default=1, help="the dimension of the image")
args = parser.parse_args()

# initialize the variables
is_trained_with_pytorch = False
is_saved_tf_model = False
is_conv = False
means = 0
stds = 0
correctly_classified_images = 0
verified_images = 0
total_images = 0
# get the params
netname = args.network
epsilon = np.float64(args.epsilon)
dataname = args.dataname
domain = args.domain
normalize_value = args.normalize
dimension = args.dimension

filename, file_extension = os.path.splitext(netname)
if file_extension == ".pyt":
    is_trained_with_pytorch = True
elif file_extension == ".meta":
    is_saved_tf_model = True
elif file_extension != ".tf":
    print("file extension not supported")
    exit(1)

if epsilon < 0 or epsilon > 1:
    print("epsilon can only be between 0 and 1")
    exit(1)

if domain != 'deepzono' and domain != 'deeppoly':
    print("domain name can be either deepzono or deeppoly")
    exit(1)

csvfile = open(dataname, 'r')
tests = csv.reader(csvfile, delimiter=',')
num_pixels = -1
for test in tests:
    num_pixels = len(test) - 1
    break


if is_saved_tf_model:
    netfolder = os.path.dirname(netname) 

    tf.logging.set_verbosity(tf.logging.ERROR)

    sess = tf.Session()
    saver = tf.train.import_meta_graph(netname)
    # saver.restore(sess, tf.train.latest_checkpoint(netfolder+'/'))
    # eran = ERAN(sess.graph.get_tensor_by_name('fully_connected/BiasAdd:0'), sess)
    saver.restore(sess, '../../networks/autumn/autumn-cnn-weights.ckpt')
    eran = ERAN(sess.graph.get_tensor_by_name('y:0'), sess)
else:
    print(num_pixels)
    model, is_conv, means, stds = read_net(netname, num_pixels, is_trained_with_pytorch)
    eran = ERAN(model)

csvfile = open(dataname, 'r')
tests = csv.reader(csvfile, delimiter=',')
for test in tests:
    start = time.time()

    image = (np.float64(test[1:len(test)]) / np.float64(255)) - normalize_value
    # print(image.shape)
    specLB = np.copy(image)
    specUB = np.copy(image)
    if is_trained_with_pytorch:
        normalize(specLB, dimension, num_pixels, means, stds)
        normalize(specUB, dimension, num_pixels, means, stds)
    
    label = eran.analyze_box(specLB, specUB, domain, int(test[0]))

    if label == int(test[0]):
        left = 0
        right = 30
        while left < right:
            mid = (left + right + 1) // 2
            # print(mid)
            epsilon = mid * 0.004
            specLB = np.clip(image - epsilon, 0-normalize_value, 1-normalize_value)
            specUB = np.clip(image + epsilon, 0-normalize_value, 1-normalize_value)

            if is_trained_with_pytorch:
                normalize(specLB, dimension, num_pixels, means, stds)
                normalize(specUB, dimension, num_pixels, means, stds)

            perturbed_label = eran.analyze_box(specLB, specUB, domain, label)
            if perturbed_label == label:
                left = mid
            else:
                right = mid - 1

        print("img", total_images, " maximum distortion: ", left, left * 0.04)
        end = time.time()
        # print(end - start)
    else:
        print("img", total_images, "not considered, correct_label", int(test[0]), "classified label ", label)
    total_images += 1

# print('analysis precision ', verified_images, '/ ', correctly_classified_images)
