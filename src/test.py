import os
import itertools
import re
import datetime
import editdistance
import numpy as np
from scipy import ndimage
import pylab
from keras import backend as K
from image_generator import TextImageGenerator
from keras.utils.data_utils import get_file
from keras.preprocessing import image
import numpy as np

img_h = 64
img_w = 128
words_per_epoch = 16000
val_split = 0.2
val_words = int(words_per_epoch * (val_split))

# Network parameters
conv_filters = 16
kernel_size = (3, 3)
pool_size = 2
time_dense_size = 32
rnn_size = 512
minibatch_size=32


fdir = os.path.dirname(get_file('wordlists.tgz',
                                origin='http://www.mythic-ai.com/datasets/wordlists.tgz', untar=True))


img_gen = TextImageGenerator(monogram_file=os.path.join(fdir, 'wordlist_mono_clean.txt'),
                             bigram_file=os.path.join(fdir, 'wordlist_bi_clean.txt'),
                             minibatch_size=minibatch_size,
                             img_w=img_w,
                             img_h=img_h,
                             downsample_factor=(pool_size ** 2),
                             val_split=words_per_epoch - val_words
                             )

img_gen.on_train_begin(save=True)
data = img_gen.next_train().next()[0]['the_input'][0]
print data
print data.shape
np.save('test.arr', data)
data2 = np.load('test.arr.npy')

print data2
print data2.shape
