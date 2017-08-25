from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten

nb_filters = 32
pool_size = (2, 2)
kernel_size1 = (3, 3)
kernel_size2 = (5, 5)

def init_model(nb_classes, input_shape):

	model = Sequential()
	
	model.add(Convolution2D(nb_filters, kernel_size1, padding='valid', input_shape=input_shape, use_bias=True))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=pool_size))

	model.add(Convolution2D(nb_filters, kernel_size2, use_bias=True, padding='valid'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=pool_size))

	model.add(Flatten())

	model.add(Dense(64))
	model.add(Activation('relu'))

	model.add(Dense(nb_classes))
	model.add(Activation('softmax'))
	return model
