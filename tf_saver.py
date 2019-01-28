import tensorflow as tf


# Create some variables.
v1 = tf.Variable(tf.random_normal([7, 2], stddev=0.35), name="v1")
v2 = tf.Variable(tf.random_normal([7, 2], stddev=0.35), name="v2")

# Add an op to initialize the variables.
init_op = tf.global_variables_initializer()

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

# Later, launch the model, initialize the variables, do some work, save the
# variables to disk.
with tf.Session() as sess:
    sess.run(init_op)
    # Do some work with the model.
    # Save the variables to disk.
    # saver.restore(sess, "tmp/model.ckpt")
    print(sess.run(v1))



