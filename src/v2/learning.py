from keras import backend as K
from keras.callbacks import TensorBoard

import image_generator3 as ig
import network

import os

img_w = img_h = 64
nb_epoch = 10
TRAINING_SET_SIZE = 100000
TEST_SET_SIZE = TRAINING_SET_SIZE / 5

K.set_learning_phase(1)
if K.image_data_format() == 'channels_first':
	input_shape = (1, img_w, img_h)
else:
	input_shape = (img_w, img_h, 1)


def train():
	(x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE)
	(x_test, y_test) = ig.get_test_set(TEST_SET_SIZE)

	model = network.init_model(ig.LABEL_SIZE, input_shape)

	print (input_shape)

	model.summary()

	model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

	tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)

	model.fit(x_train, y_train, batch_size=32, epochs=nb_epoch,
	          verbose=1, validation_split=0.15, callbacks=[tensorboard])

	score = model.evaluate(x_test, y_test)

	print('test score: ', score[0])
	print('test accuracy: ', score[1])


	if not os.path.exists('results/data'):
		os.makedirs('results/data')
	model.save_weights('results/data/model.h5')


if __name__ == '__main__':
	train()
