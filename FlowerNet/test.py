import Image
import numpy as np
import tensorflow as tf


def number_of_0(x):
    if 1 <= x <= 9:
        return 3
    elif 10 <= x <= 99:
        return 2
    elif 100 <= x <= 999:
        return 1
    else:
        return 0


def convert_to_one_hot(y, C):
    return np.eye(C)[y.reshape(-1)].T


def predict(X_test, Y_test):

    with tf.Session() as sess:

        saver = tf.train.import_meta_graph("model/model.ckpt.meta")
        saver.restore(sess, tf.train.latest_checkpoint('model/'))

        graph = tf.get_default_graph()

        # print([n.name for n in tf.get_default_graph().as_graph_def().node])

        X = graph.get_tensor_by_name("X:0")
        Y = graph.get_tensor_by_name("Y:0")

        Z3 = graph.get_tensor_by_name("fully_connected/BiasAdd:0")
        # print(sess.run(Z3))
        feed_dict = {X: X_test, Y: Y_test}
        print(sess.run(Z3, feed_dict))


def get_train_dataset():
    x = np.zeros([1, 64, 64, 3])
    new_pic_path = r'C:\Users\JohnReese\Desktop\CSV\flowers\image_0001.jpg'
    pid = 1
    im = Image.open(new_pic_path)
    x[0] = np.array(im) / 255.0

    y = np.array([int((pid+79)/80)-1])
    y = convert_to_one_hot(y, 6).T
    print(y)
    return x, y


X, Y = get_train_dataset()
predict(X, Y)





