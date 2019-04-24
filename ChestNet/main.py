"""
.....
"""
if file_extension == ".pyt":
    is_trained_with_pytorch = True
elif file_extension == ".meta" or file_extension == ".h5":
    is_saved_tf_model = True
elif file_extension != ".tf":
    print("file extension not supported")
    exit(1)


"""
.....
"""

if is_saved_tf_model:
    eran = ERAN(tf.keras.models.load_model(netname))
else:
    print(num_pixels)
    model, is_conv, means, stds = read_net(netname, num_pixels, is_trained_with_pytorch)
    eran = ERAN(model)

"""
.....
"""