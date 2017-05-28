from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import regularizers

nb_filters = 32
pool_size = (2, 2)
kernel_size = (3, 3)


def init_model(nb_classes, input_shape):
	model = Sequential()
	
	model = Sequential()
	
	model.add(Convolution2D(16, kernel_size, padding='valid', input_shape=input_shape, use_bias=True))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=pool_size))

	model.add(Convolution2D(nb_filters, kernel_size, use_bias=True, padding='valid'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=pool_size))

	model.add(Flatten())

	model.add(Dense(512))
	model.add(Activation('relu'))
	model.add(Dropout(0.1))

	model.add(Dense(nb_classes))
	model.add(Activation('softmax'))

	return model
