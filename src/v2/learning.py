from keras import backend as K
from keras.callbacks import TensorBoard

import image_generator as ig
import network

import os

img_w = img_h = 64
nb_epoch = 1
TRAINING_SET_SIZE = 50000
TEST_SET_SIZE = TRAINING_SET_SIZE / 5

K.set_learning_phase(1)
if K.image_data_format() == 'channels_first':
  input_shape = (1, img_w, img_h)
else:
  input_shape = (img_w, img_h, 1)


def train():

  model = network.init_model(ig.LABEL_SIZE, input_shape)

  model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

  tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)


  epoch = 0
  (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE, blur=True)
  model.fit(x_train, y_train, batch_size=32, epochs=epoch + nb_epoch,
            verbose=1, validation_split=0.2, callbacks=[tensorboard], initial_epoch = epoch)

  epoch += nb_epoch
  (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE, blur=True, ud = True)
  model.fit(x_train, y_train, batch_size=32, epochs=epoch + nb_epoch,
            verbose=1, validation_split=0.2, callbacks=[tensorboard], initial_epoch = epoch)

  epoch += nb_epoch
  (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE, blur=True, ud = True, multi_sizes=True)
  model.fit(x_train, y_train, batch_size=32, epochs=epoch + nb_epoch,
            verbose=1, validation_split=0.2, callbacks=[tensorboard], initial_epoch = epoch)

  epoch += nb_epoch
  (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE, blur=True, ud = True, multi_sizes=True, multi_fonts=True)
  model.fit(x_train, y_train, batch_size=32, epochs=epoch + nb_epoch,
            verbose=1, validation_split=0.2, callbacks=[tensorboard], initial_epoch = epoch)

  epoch += nb_epoch
  (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE, blur=True, ud = True, multi_sizes=True, multi_fonts=True, rotate=True)
  model.fit(x_train, y_train, batch_size=32, epochs=epoch + nb_epoch,
            verbose=1, validation_split=0.2, callbacks=[tensorboard], initial_epoch = epoch)

  (x_test, y_test) = ig.get_test_set(TEST_SET_SIZE)
  score = model.evaluate(x_test, y_test)
  print "\n"
  print 'Test score: {0:.4g}'.format(score[0]) 
  print 'Test accur: {0:.4g}'.format(score[1])

  if not os.path.exists('results/data'):
    os.makedirs('results/data')
  model.save_weights('results/data/model.h5')

if __name__ == '__main__':
  train()
