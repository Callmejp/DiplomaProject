import tensorflow as tf
import numpy as np
import Image
from transform import number_of_0


def convert_to_one_hot(y, C):
    return np.eye(C)[y.reshape(-1)].T


def predict(X_test, Y_test):

    with tf.Session() as sess:

        saver = tf.train.import_meta_graph("model/model.ckpt.meta")
        saver.restore(sess, tf.train.latest_checkpoint('model/'))

        graph = tf.get_default_graph()

        X = graph.get_tensor_by_name("X:0")
        Y = graph.get_tensor_by_name("Y:0")

        Z3 = graph.get_tensor_by_name("fully_connected/BiasAdd:0")
        # print(sess.run(Z3))
        feed_dict = {X: X_test, Y: Y_test}
        print(sess.run(Z3, feed_dict))


def get_train_dataset(pid):
    x = np.zeros([1, 64, 64, 3])
    length = number_of_0(pid)
    s0 = ""
    for j in range(length):
        s0 += "0"
    image_name = 'image_' + s0 + str(pid) + '.jpg'
    new_pic_path = 'flowers/' + image_name

    im = Image.open(new_pic_path)
    x[0] = np.array(im) / 255.0

    y = np.array([int((pid+79)/80)-1])
    y = convert_to_one_hot(y, 6).T
    print(y)
    return x, y


if __name__ == "__main__":
    X, Y = get_train_dataset(80)
    predict(X, Y)





