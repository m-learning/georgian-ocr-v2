#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import itertools
import numpy as np
import cairocffi as cairo
from keras import backend as K
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Input, Dense, Activation
from keras.layers import Reshape, Lambda
from keras.layers.merge import add, concatenate
from keras.models import Model
from keras.layers.recurrent import GRU
from keras.optimizers import SGD
from keras.utils.data_utils import get_file
import fragmenter as f

OUTPUT_DIR = 'results'
SEPARATOR = '\n'

latin_upper = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
latin_lower = u'abcdefghijklmnopqrstuvwxyz'
georgian = u'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰჱჲჳჴჵ'
numbers = u'1234567890'
symbols = u'!@#$%^&*()-+=/\\.,<>?;:"|}{[]'
blank = u' '

chars = georgian + \
        numbers + \
        symbols + \
        blank

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    # the 2 is critical here since the first couple outputs of the RNN
    # tend to be garbage:
    y_pred = y_pred[:, 2:, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


# For a real OCR application, this should be beam search with a dictionary
# and language model.  For this example, best path is sufficient.

def decode_batch(prediction):
    ret = []
    for j in range(prediction.shape[0]):
        out_best = list(np.argmax(prediction[j, 2:], 1))
        out_best = [k for k, g in itertools.groupby(out_best)]
        # 26 is space, 27 is CTC blank char
        outstr = ''
        for c in out_best:
            if c >= 0 and c < len(chars) -3:
                outstr += chars[c]
            elif c == len(chars) - 2:
                outstr += ' '
        ret.append(outstr)
    return ret


def predict_text(model, image, w, h):
    surface = cairo.ImageSurface.create_from_png(image)
    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (h, w, 4)
    a = a[:, :, 0]  # grab single channel
    a = a.astype(np.float32) / 255
    a = np.expand_dims(a, 0)

    if K.image_data_format() == 'channels_first':
        X_data = np.ones([1, 1, w, h])
    else:
        X_data = np.ones([1, w, h, 1])

    if K.image_data_format() == 'channels_first':
        X_data[0, 0, 0:w, :] = a[0, :, :].T
    else:
        X_data[0, 0:w, :, 0] = a[0, :, :].T
    prediction = model.predict(X_data, batch_size=1, verbose=0)

    return decode_batch(prediction)


def init_arguments():

    parser = argparse.ArgumentParser(description='Georgian OCR')
    parser.add_argument('-i', '--image', metavar='image_path', type=str,
                        help='Path to the image to recognize.')
    parser.add_argument('-W', '--weights', metavar='weights_path', type=str,
                        help='Path to the weights.')
    parser.add_argument('-w', '--width', metavar='image_width', type=int,
                        help='image width: 64 / 128 / 256 / 512 (256 is default)', default=64)
    parser.add_argument('-m', '--model', metavar='model', type=str,
                        help='Path to model')
    parser.add_argument('-e', '--english', action='store_true',
                        help='print output in english letters')
    return parser.parse_args()


def get_model(img_w, weight_file_name):

    # Input Parameters
    img_h = 64
    words_per_epoch = 1600
    val_split = 0.2
    val_words = int(words_per_epoch * (val_split))

    # Network parameters
    conv_filters = 16
    kernel_size = (3, 3)
    pool_size = 2
    time_dense_size = 32
    rnn_size = 512
    minibatch_size=32

    if K.image_data_format() == 'channels_first':
        input_shape = (1, img_w, img_h)
    else:
        input_shape = (img_w, img_h, 1)

    act = 'relu'
    input_data = Input(name='the_input', shape=input_shape, dtype='float32')
    inner = Conv2D(conv_filters, kernel_size, padding='same',
                   activation=act, kernel_initializer='he_normal',
                   name='conv1')(input_data)
    inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max1')(inner)
    inner = Conv2D(conv_filters, kernel_size, padding='same',
                   activation=act, kernel_initializer='he_normal',
                   name='conv2')(inner)
    inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max2')(inner)

    conv_to_rnn_dims = (img_w // (pool_size ** 2), (img_h // (pool_size ** 2)) * conv_filters)
    inner = Reshape(target_shape=conv_to_rnn_dims, name='reshape')(inner)

    inner = Dense(time_dense_size, activation=act, name='dense1')(inner)

    gru_1 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru1')(inner)
    gru_1b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru1_b')(inner)
    gru1_merged = add([gru_1, gru_1b])
    gru_2 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru2')(gru1_merged)
    gru_2b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(gru1_merged)

    inner = Dense(28, kernel_initializer='he_normal',
                  name='dense2')(concatenate([gru_2, gru_2b]))
    y_pred = Activation('softmax', name='softmax')(inner)
    model = Model(inputs=input_data, outputs=y_pred)
    model.summary()

    weight_file = os.path.join(OUTPUT_DIR, os.path.join(run_name, weight_file_name))
    model.load_weights(weight_file)

    #test_func = K.function([input_data], [y_pred])

    return model


if __name__ == '__main__':
    # Download model.
    epoch_version = 25
    img_h = 64
    weight_file_name = 'weights%02d.h5' % (epoch_version - 1)
    model_url = 'http://data.grid.ge/ocr/v2/' + weight_file_name
    get_file(weight_file_name, origin=model_url, cache_dir='.', cache_subdir=OUTPUT_DIR + "/data")
    run_name = 'data'
    args = init_arguments()

    f.do_fragmentation(args.image)
    model = get_model(args.width, weight_file_name)
    result = ''
    for (dir_path, dir_names, file_names) in os.walk(f.FRAGMENTS_DIR):
        file_names = sorted(file_names)
        for file_name in file_names:
            print file_name + ': ' + predict_text(model, os.path.join(dir_path, file_name), args.width, img_h)[0] + SEPARATOR
        break

    #print(result)
    # predict(19, 128, args.image)
