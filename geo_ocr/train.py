from keras import backend as K
from keras.callbacks import TensorBoard
import tensorflow as tf
import image_generator as ig
import network

import os

img_w = img_h = 64
nb_epoch = 1
TRAINING_SET_SIZE = 20000

SCORE_PATH = "score.txt"

TEST_SET_SIZE = 2000

final_model = []

K.set_learning_phase(1)
if K.image_data_format() == 'channels_first':
    input_shape = (1, img_w, img_h)
else:
    input_shape = (img_w, img_h, 1)

batch_size = [16, 25, 32]
nb_epoch_t = [20, 25, 32]
optimizer = ["adadelta", "adam", "rmsprop"]

try:
    os.remove(SCORE_PATH)
except OSError:
    pass


def train():
    path = os.getcwd()

    tensorboard = TensorBoard(log_dir=os.path.join(path, 'logs'),
                              histogram_freq=0, write_graph=True,
                              write_images=True)

    for each_batch in batch_size:
        for each_epoch in nb_epoch_t:
            for each_optimizer in optimizer:

                tmp_model = [each_batch, each_epoch, each_optimizer]

                model = network.init_model(each_optimizer)

                for epoch in range(0, each_epoch, nb_epoch):
                    (x_train, y_train) = ig.next_batch(TRAINING_SET_SIZE,
                                                       rotate=True, ud=True, lr=True,
                                                       multi_fonts=True,
                                                       multi_sizes=True, blur=False)
                    model.fit(x_train, y_train,
                              batch_size=each_batch, epochs=epoch + nb_epoch,
                              verbose=1, validation_split=0.1,
                              callbacks=[tensorboard], initial_epoch=epoch)

                    if not os.path.exists(os.path.join(path, 'results/data')):
                        os.makedirs(os.path.join(path, 'results/data'))
                    model.save_weights(os.path.join(path,
                                                    'results/data/model.h5'))

                (x_test, y_test) = ig.next_batch(TEST_SET_SIZE)
                score = model.evaluate(x_test, y_test)

                tmp_model.append(score[0])
                tmp_model.append(score[1])

                tf.train.write_graph(K.get_session().graph, "results/data", "model.pb", False)

                final_model.append(tmp_model)

                print "\n"
                print 'Test score: {0:.4g}'.format(score[0])
                print 'Test accur: {0:.4g}'.format(score[1])

    final_model.sort(key=lambda row: row[3])

    with open(SCORE_PATH, "a") as myfile:
        for each in final_model:
            myfile.write(str(each) + "  ")
            myfile.write("\n")

if __name__ == '__main__':
    train()