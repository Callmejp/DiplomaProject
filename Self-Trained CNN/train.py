import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import Image
import math
from transform import number_of_0


def convert_to_one_hot(y, C):
    return np.eye(C)[y.reshape(-1)].T


def random_mini_batches(X, Y, mini_batch_size=64, seed=0):
    np.random.seed(seed)
    m = X.shape[0]
    mini_batches = []

    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation, :, :, :]
    shuffled_Y = Y[permutation, :]

    num_complete_minibatches = int(math.floor(m / mini_batch_size))
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size: (k + 1) * mini_batch_size, :, :, :]
        mini_batch_Y = shuffled_Y[k * mini_batch_size: (k + 1) * mini_batch_size, :]

        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size - m:, :, :, :]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size - m:, :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches


def create_placeholders(n_h0, n_w0, n_c0, n_y):
    x = tf.placeholder(dtype=tf.float32, shape=[None, n_h0, n_w0, n_c0], name="X")
    y = tf.placeholder(dtype=tf.float32, shape=[None, n_y], name="Y")

    return x, y


def initialize_parameters():
    tf.set_random_seed(1)

    W1 = tf.get_variable("W1", [4, 4, 3, 8], initializer=tf.contrib.layers.xavier_initializer(seed=0))
    W2 = tf.get_variable("W2", [2, 2, 8, 16], initializer=tf.contrib.layers.xavier_initializer(seed=0))

    parameters = {"W1": W1, "W2": W2}
    return parameters


def forward_propagation(X, parameters):
    W1 = parameters['W1']
    W2 = parameters['W2']

    Z1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
    A1 = tf.nn.relu(Z1)
    P1 = tf.nn.max_pool(A1, ksize=[1, 8, 8, 1], strides=[1, 8, 8, 1], padding='SAME')

    Z2 = tf.nn.conv2d(P1, W2, strides=[1, 1, 1, 1], padding='SAME')
    A2 = tf.nn.relu(Z2)
    P2 = tf.nn.max_pool(A2, ksize=[1, 4, 4, 1], strides=[1, 4, 4, 1], padding='SAME')

    P2 = tf.contrib.layers.flatten(P2)
    Z3 = tf.contrib.layers.fully_connected(P2, 6, activation_fn=None)

    return Z3


def compute_cost(Z3, Y):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=Z3, labels=Y))
    return cost


def model(X_train, Y_train, learning_rate=0.009, num_epochs=90, minibatch_size=64, print_cost=True):
    tf.set_random_seed(1)
    seed = 3
    (m, n_H0, n_W0, n_C0) = X_train.shape
    n_y = Y_train.shape[1]
    costs = []

    X, Y = create_placeholders(n_H0, n_W0, n_C0, n_y)
    parameters = initialize_parameters()
    Z3 = forward_propagation(X, parameters)


    cost = compute_cost(Z3, Y)
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    init = tf.global_variables_initializer()

    saver = tf.train.Saver()

    with tf.Session() as sess:

        sess.run(init)
        print(Z3.name)
        exit(0)
        for epoch in range(num_epochs):

            minibatch_cost = 0.
            num_minibatches = int(m / minibatch_size)
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)

            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _, temp_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})

                minibatch_cost += temp_cost / num_minibatches

            if print_cost and epoch % 5 == 0:
                print("Cost after epoch %i: %f" % (epoch, minibatch_cost))
            if print_cost and epoch % 1 == 0:
                costs.append(minibatch_cost)

        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        predict_op = tf.argmax(Z3, 1)
        correct_prediction = tf.equal(predict_op, tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print(accuracy)
        train_accuracy = accuracy.eval({X: X_train, Y: Y_train})
        print("Train Accuracy:", train_accuracy)

        saver.save(sess, 'model/model.ckpt')

        return train_accuracy, parameters


def get_train_dataset():
    x = np.zeros([480, 64, 64, 3])

    for i in range(1, 481):
        length = number_of_0(i)
        s0 = ""
        for j in range(length):
            s0 += "0"
        image_name = 'image_' + s0 + str(i) + '.jpg'
        new_pic_path = 'flowers/' + image_name

        im = Image.open(new_pic_path)
        im = np.array(im)
        x[i - 1] = im
    x /= 255.0
    # print(X[15])
    # plt.imshow(X[15])
    # plt.show()
    y = np.zeros(480, dtype=int).reshape(1, 480)
    for i in range(1, 6):
        y[0, i * 80:(i + 1) * 80] = i
    y = convert_to_one_hot(y, 6).T
    # print(y)
    # print(Y.shape)
    return x, y


if __name__ == "__main__":
    X, Y = get_train_dataset()
    _, parameters = model(X, Y)





