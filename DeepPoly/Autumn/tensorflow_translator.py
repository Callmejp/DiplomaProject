'''
@author: Adrian Hoffmann
'''
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.engine.sequential import Sequential
from tensorflow.python.framework import graph_util
######################################
"""
Because in line 195
Autumn(model)'s op.outputs.shape isn't explict
so l calculated manually the dimensions of each matrix here
"""
autumn_shape_dict = {
    "import/x": [1, 66, 200, 3],
    "import/Conv2D": [1, 31, 98, 24],
    "import/add": [1, 31, 98, 24],
    "import/Relu": [1, 31, 98, 24],
    "import/Conv2D_1": [1, 14, 47, 36],
    "import/add_1": [1, 14, 47, 36],
    "import/Relu_1": [1, 14, 47, 36],
    "import/Conv2D_2": [1, 5, 22, 48],
    "import/add_2": [1, 5, 22, 48],
    "import/Relu_2": [1, 5, 22, 48],
    "import/Conv2D_3": [1, 3, 20, 64],
    "import/add_3": [1, 3, 20, 64],
    "import/Relu_3": [1, 3, 20, 64],
    "import/Conv2D_4": [1, 1, 18, 64],
    "import/add_4": [1, 1, 18, 64],
    "import/Relu_4": [1, 1, 18, 64],
    "import/MatMul": [1, 1164],
    "import/add_5": [1, 1164],
    "import/Relu_5": [1, 1164]
}
######################################

def tensorshape_to_intlist(tensorshape):
    """
    TensorFlow has its own wrapper for shapes because some entries could be None. This function turns them into int-lists. None will become a 1.

    Arguments
    ---------
    tensorshape : tf.TensorShape

    Return
    ------
    output : list
        list of ints corresponding to tensorshape
    """
    try:
        tmp = list(map(lambda j: 1 if j.value is None else int(j), tensorshape))
    except Exception as e:
        # print(e)
        tmp = [1, 66, 200, 3]
    return tmp


class TFTranslator:
    """
    This class is used to turn a TensorFlow model into two lists that then can be processed by an Optimizer object
    """

    def __init__(self, model, session=None):
        """
        This constructor takes a reference to a TensorFlow Operation or Tensor or Keras model and then applies the two TensorFlow functions
        graph_util.convert_variables_to_constants and graph_util.remove_training_nodes to cleanse the graph of any nodes that are linked to training. This leaves us with
        the nodes you need for inference.
        In the resulting graph there should only be tf.Operations left that have one of the following types [Const, MatMul, Add, BiasAdd, Conv2D, Reshape, MaxPool, Placeholder, Relu, Sigmoid, Tanh]
        If the input should be a Keras model we will ignore operations with type Pack, Shape, StridedSlice, and Prod such that the Flatten layer can be used.

        Arguments
        ---------
        model : tensorflow.Tensor or tensorflow.Operation or tensorflow.python.keras.engine.sequential.Sequential or keras.engine.sequential.Sequential
            if tensorflow.Tensor: model.op will be treated as the output node of the TensorFlow model. Make sure that the graph only contains supported operations after applying
                                  graph_util.convert_variables_to_constants and graph_util.remove_training_nodes with [model.op.name] as output_node_names
            if tensorflow.Operation: model will be treated as the output of the TensorFlow model. Make sure that the graph only contains supported operations after applying
                                  graph_util.convert_variables_to_constants and graph_util.remove_training_nodes with [model.op.name] as output_node_names
            if tensorflow.python.keras.engine.sequential.Sequential: x = model.layers[-1].output.op.inputs[0].op will be treated as the output node of the Keras model. Make sure that the graph only
                                  contains supported operations after applying graph_util.convert_variables_to_constants and graph_util.remove_training_nodes with [x.name] as
                                  output_node_names
            if keras.engine.sequential.Sequential: x = model.layers[-1].output.op.inputs[0].op will be treated as the output node of the Keras model. Make sure that the graph only
                                  contains supported operations after applying graph_util.convert_variables_to_constants and graph_util.remove_training_nodes with [x.name] as
                                  output_node_names
        session : tf.Session
            session which contains the information about the trained variables. If None the code will take the Session from tf.get_default_session(). If you pass a keras model you don't have to
            provide a session, this function will automatically get it.
        """
        output_names = None
        if issubclass(model.__class__, tf.Tensor):
            output_names = [model.op.name]
        elif issubclass(model.__class__, tf.Operation):
            output_names = [model.name]
        elif issubclass(model.__class__, Sequential):
            session = tf.keras.backend.get_session()
            output_names = [model.layers[-1].output.op.inputs[0].op.name]
            model = model.layers[-1].output.op
        else:
            import keras
            if issubclass(model.__class__, keras.engine.sequential.Sequential):
                session = keras.backend.get_session()
                output_names = [model.layers[-1].output.op.inputs[0].op.name]
                model = model.layers[-1].output.op
            else:
                assert 0, "ERAN can't recognize this input"

        if session is None:
            session = tf.get_default_session()

        tmp = graph_util.convert_variables_to_constants(session, model.graph.as_graph_def(), output_names)
        # print(tmp)
        self.graph_def = graph_util.remove_training_nodes(tmp)

    # print(self.graph_def)



    def translate(self):
        """
        The constructor has produced a graph_def with the help of the functions graph_util.convert_variables_to_constants and graph_util.remove_training_nodes.
        translate() takes that graph_def, imports it, and translates it into two lists which then can be processed by an Optimzer object.

        Return
        ------
        (operation_types, operation_resources) : (list, list)
            A tuple with two lists, the first one has items of type str and the second one of type dict. In the first list the operation types are stored (like "Add", "MatMul", etc.).
            In the second list we store the resources (matrices, biases, etc.) for those operations. It is organised as follows: operation_resources[i][domain] has the resources related to
            operation_types[i] when analyzed with domain (domain is currently either 'deepzono' or 'deeppoly', as of 8/30/18)
        """
        operation_types = []
        operation_resources = []
        reshape_map = {}
        operations_to_be_ignored = ["Reshape", "Pack", "Shape", "StridedSlice", "Prod", "ConcatV2"]
        ############################################
        relu_cnt = 0
        last_op = None
        step = 0
        ############################################
        with tf.Graph().as_default() as graph:
            with tf.Session() as sess:
                self.sess = sess
                tf.import_graph_def(self.graph_def)
                for op in graph.get_operations():
                    ############################################
                    # print(op.name, op.type)
                    if relu_cnt >= 6:
                        if step == 0 and op.type != "MatMul":
                            continue
                        elif op.type == "MatMul" or op.type == "Add" or op.type == "Relu":
                            operation_types.append(op.type)
                            input_tensor_names = []
                            deeppoly_res = ()
                            if step == 0:
                                # MatMul: use the last relu result as input
                                input_tensor_names = [last_op.name]
                                deeppoly_res = self.matmul_resources(op)
                            elif step == 1:
                                # Add: as normal
                                input_tensor_names = [op.inputs[0].name]
                                deeppoly_res = self.add_resources(op)
                            elif step == 2:
                                # Relu:
                                input_tensor_names = [op.inputs[0].name]
                                step = -1
                                last_op = op
                            step += 1
                            in_out_info = (
                            input_tensor_names, op.outputs[0].name, tensorshape_to_intlist(op.outputs[0].shape))
                            deepzono_res = deeppoly_res + in_out_info
                            operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                        continue
                    print(op.name, op.type)
                    ############################################
                    if op.type == "Const":
                        continue
                    elif op.type in operations_to_be_ignored:
                        input_name = op.inputs[0].name
                        output_name = op.outputs[0].name
                        kind = op.inputs[0].op.type
                        # print(input_name, output_name, kind)
                        if kind in operations_to_be_ignored:
                            reshape_map[output_name] = reshape_map[input_name]
                        else:
                            reshape_map[output_name] = input_name
                        continue

                    operation_types.append(op.type)
                    input_tensor_names = []
                    for inp in op.inputs:
                        name = inp.name
                        kind = inp.op.type
                        if kind in operations_to_be_ignored:
                            name = reshape_map[name]
                        if kind == 'Const':
                            continue
                        input_tensor_names.append(name)
                    ############################################
                    in_out_info = (input_tensor_names, op.outputs[0].name, autumn_shape_dict[op.name])
                    ############################################
                    if op.type == "MatMul":
                        # print(in_out_info)
                        deeppoly_res = self.matmul_resources(op)
                        deepzono_res = deeppoly_res + in_out_info
                        operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                    elif op.type == "Add":
                        left_type = op.inputs[0].op.type
                        right_type = op.inputs[1].op.type
                        if left_type == 'Const' and right_type == 'Const':
                            assert 0, "we don't support the addition of two constants yet"
                        elif left_type == 'Const' or right_type == 'Const':
                            deeppoly_res = self.add_resources(op)
                            deepzono_res = deeppoly_res + in_out_info
                            operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                        else:
                            operation_types[-1] = "Resadd"
                            operation_resources.append({'deepzono': in_out_info})
                    elif op.type == "BiasAdd":
                        if op.inputs[1].op.type == 'Const':
                            deeppoly_res = self.add_resources(op)
                            deepzono_res = deeppoly_res + in_out_info
                            operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                        else:
                            assert 0, "this bias add doesn't meet our assumption (bias is constant)"
                    elif op.type == "Conv2D":
                        ############################################
                        filters, image_shape, strides, padding = self.conv2d_resources(op, 1)
                        ############################################
                        deeppoly_res = (filters, image_shape, strides, padding)
                        deepzono_res = deeppoly_res + in_out_info
                        operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                    elif op.type == "MaxPool":
                        image_shape, window_size, strides, padding = self.maxpool_resources(op)
                        deeppoly_res = (image_shape, window_size, in_out_info[2])
                        deepzono_res = (image_shape, window_size, strides, padding) + in_out_info
                        operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                    elif op.type == "Placeholder":
                        deeppoly_res = ()
                        deepzono_res = in_out_info
                        operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                    elif op.type in ["Relu", "Sigmoid", "Tanh"]:
                        ############################################
                        relu_cnt += 1
                        if relu_cnt >= 6:
                            last_op = op
                        ############################################
                        deeppoly_res = self.nonlinearity_resources(op)
                        deepzono_res = deeppoly_res + in_out_info
                        operation_resources.append({'deepzono': deepzono_res, 'deeppoly': deeppoly_res})
                    # elif op.type == "ConcatV2":
                    #	print("Concatv2")
                    #	deeppoly_res = self.concat_resources(op)
                    #	deepzono_res = deeppoly_res + in_out_info
                    #	operation_resources.append({'deepzono':deepzono_res, 'deeppoly':deeppoly_res})
                    else:
                        # print("operation type1 ",in_out_info,op.inputs[0].shape,op.inputs[1].shape)
                        assert 0, "Operations of type " + op.type + " are not yet supported."

                return operation_types, operation_resources

    def matmul_resources(self, op):
        """
        checks which one of the direct ancestor tf.Operations is a constant and returns the underlying tensor as a numpy.ndarray inside a tuple. The matrix is manipulated in a way that it can be
        used as the left multiplier in the matrix multiplication.

        Arguments
        ---------
        op : tf.Operation
            must have type "MatMul"

        Return
        ------
        output : tuple
            tuple with the matrix (of type numpy.ndarray) as its only item
        """

        inputs = op.inputs
        left = inputs[0]
        right = inputs[1]
        # print("inputs:", left.name, right.name)
        if left.op.type == "Const":
            print("wrong")
            matrix = self.sess.run(left) if not op.get_attr("transpose_a") else self.sess.run(left).transpose()
        else:
            matrix = self.sess.run(right).transpose() if not op.get_attr("transpose_b") else self.sess.run(right)

        return (matrix,)

    def add_resources(self, op):
        """
        checks which one of the direct ancestor tf.Operations is a constant and returns the underlying tensor as a numpy.ndarray inside a tuple.

        Arguments
        ---------
        op : tf.Operation
            must have type "Add"

        Return
        ------
        output : tuple
            tuple with the addend (of type numpy.ndarray) as its only item
        """
        inputs = op.inputs
        left = inputs[0]
        right = inputs[1]
        # print("inputs:", left, right)

        if left.op.type == "Const":
            addend = self.sess.run(left)
        else:
            addend = self.sess.run(right)

        return (addend,)

    def conv2d_resources(self, op, flag=0):
        """
        Extracts the filter, the stride of the filter, and the padding from op as well as the shape of the input coming into op

        Arguments
        ---------
        op : tf.Operation
            must have type "Conv2D"

        Return
        ------
        output : tuple
            has 4 entries (numpy.ndarray, numpy.ndarray, numpy.ndarray, str)
        """
        ############################################
        inputs = op.inputs
        image = inputs[0]
        filters = inputs[1]
        # print(image.name)
        filters = self.sess.run(filters)
        image_shape = tensorshape_to_intlist(image.shape)[1:]
        if flag == 1:
            # print(image.name[:-2])
            image_shape = autumn_shape_dict[image.name[:-2]][1:]
        ############################################
        strides = op.get_attr('strides')[1:3]
        padding = op.get_attr('padding').decode('utf-8')
        return filters, image_shape, strides, padding

    def maxpool_resources(self, op):
        """
        Extracts the incoming image size (heigth, width, channels), the size of the maxpool window (heigth, width), and the strides of the window (heigth, width)

        Arguments
        ---------
        op : tf.Operation
            must have type "MaxPool"

        Return
        ------
        output : tuple
            has 4 entries - (list, numpy.ndarray, numpy.ndarray, str)
        """
        image = op.inputs[0]

        image_shape = tensorshape_to_intlist(image.shape)[1:]
        window_size = op.get_attr('ksize')[1:3]
        strides = op.get_attr('strides')[1:3]
        padding = op.get_attr('padding').decode('utf-8')

        return image_shape, window_size, strides, padding

    def nonlinearity_resources(self, op):
        """
        This function only outputs an empty tuple, to make the code look more consistent

        Return
        ------
        output : tuple
            but is empty
        """
        return ()

