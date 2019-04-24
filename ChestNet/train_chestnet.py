import tensorflow.keras
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, MaxPooling2D, Conv2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint


train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)


train_set = train_datagen.flow_from_directory(
    r'C:\Users\13217\Desktop\CNN\chest-xray\chest_xray\train',
    target_size=(64, 64),
    batch_size=32,
    color_mode="grayscale",
    class_mode='categorical'
)
test_set = test_datagen.flow_from_directory(
    r'C:\Users\13217\Desktop\CNN\chest-xray\chest_xray\test',
    target_size=(64, 64),
    batch_size=32,
    color_mode="grayscale",
    class_mode='categorical'
)


classifier = Sequential()
classifier.add(Conv2D(filters=8, kernel_size=(3,3), strides=(1,1), padding='valid', input_shape=(64,64,1), activation='relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2), strides=(2,2)))
classifier.add(Conv2D(filters=8, kernel_size=(2,2), strides=(1,1), padding='valid', activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))
classifier.add(Conv2D(filters=16, kernel_size=(4,4), strides=(1,1), padding='valid', activation='relu'))
classifier.add(MaxPooling2D(pool_size=(3, 3), strides=(3,3)))
classifier.add(Flatten())
#classifier.add(Dense(units=256, activation='relu'))
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=2, activation='softmax'))

classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
classifier.summary()


filepath="model_{epoch:02d}-{val_acc:.2f}.h5"
checkpoint = ModelCheckpoint('csv/'+filepath, monitor='val_acc',verbose=1, save_best_only=True)

classifier.fit_generator(
    train_set,
    epochs=10,
    steps_per_epoch=163,
    verbose=2,
    validation_data=test_set,
    validation_steps=624,
    callbacks=[checkpoint]
)

classifier.save('1D_binary.h5')







