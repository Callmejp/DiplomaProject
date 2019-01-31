import tensorflow as tf
from scipy import misc
from keras.models import model_from_json


class AutumnModel(object):
    def __init__(self, cnn_graph, cnn_weights):
        sess = tf.InteractiveSession()
        saver = tf.train.import_meta_graph(cnn_graph)
        saver.restore(sess, cnn_weights)
        self.cnn = tf.get_default_graph()

        self.fc3 = self.cnn.get_tensor_by_name("fc3/mul:0")
        self.y = self.cnn.get_tensor_by_name("y:0")
        self.x = self.cnn.get_tensor_by_name("x:0")
        self.keep_prob = self.cnn.get_tensor_by_name("keep_prob:0")

        # with open(lstm_json, 'r') as f:
        #     json_string = f.read()
        # self.model = model_from_json(json_string)
        # self.model.load_weights(lstm_weights)

        self.prev_image = None
        self.last = []
        self.steps = []

    def predict(self, img_path):
        image = misc.imread(img_path)
        cnn_output = self.fc3.eval(feed_dict={self.x: [image], self.keep_prob: 1.0})
        self.steps.append(cnn_output)
        if len(self.steps) > 100:
            self.steps.pop(0)
        output = self.y.eval(feed_dict={self.x: [image], self.keep_prob: 1.0})
        return output[0][0]


if __name__ == '__main__':
    cnn_graph_path = 'model/autumn-cnn-model-tf.meta'
    cnn_weights_path = 'model/autumn-cnn-weights.ckpt'
    # l find that this program can run with out sth about keras
    # lstm_json_path = 'model/autumn-lstm-model-keras.json'
    # lstm_weights_path = 'model/autumn-lstm-weights.hdf5'
    autumn = AutumnModel(cnn_graph_path, cnn_weights_path)
    for i in range(1, 17):
        image_path = 'tmp_right_save/' + str(i) + '.jpg'
        angle = autumn.predict(image_path)
        print(angle)
