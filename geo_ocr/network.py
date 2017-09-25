from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import backend as K
import image_generator as ig


img_w = img_h = 64
K.set_learning_phase(1)
if K.image_data_format() == 'channels_first':
    input_shape = (1, img_w, img_h)
else:
    input_shape = (img_w, img_h, 1)


nb_filters = 16
pool_size = (2, 2)
kernel_size = (5, 5)


def init_model(optimizer):

    model = Sequential()
    model.add(Convolution2D(16, kernel_size, padding='valid', input_shape=input_shape, use_bias=True))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))

    model.add(Convolution2D(32, kernel_size, use_bias=True, padding='valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))

    model.add(Flatten())

    model.add(Dense(1024))
    model.add(Activation('relu'))

    model.add(Dense(ig.LABEL_SIZE))
    model.add(Activation('sigmoid'))
    model.summary()

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer, metrics=['accuracy'])
    return model

