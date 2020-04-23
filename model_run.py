

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, CuDNNLSTM
import gaussian_nll as gauss
from keras import losses

from NN_preprocessing import new_preprocessing as prep
import numpy as np
import pdb
import pprint as pp

rel_path = './music_short/fav/'
scores = prep.loadScores(rel_path)
i ,o = prep.make_food(scores)

i = np.array(i)
o = np.array(o)

i = np.reshape(i, (40,100,140))
o = np.reshape(o, (40,100,140))

in_sh = i.shape
if __name__ == "__main__":

    model = Sequential()
    model.add(LSTM(70, input_shape=in_sh[1:], activation='relu', return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(128,activation = 'relu',return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(128,activation = 'relu', return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(128,activation = 'relu', return_sequences = True))
    model.add(Dropout(0.2))

    model.add(Dense(140,activation = 'softmax')) # >>> odpowiada za ostatni shape.

    f_loss = 'categorical_crossentropy'
    opt = tf.keras.optimizers.Adam(lr=1e-4, decay=1e-6)

    model.compile(loss=f_loss,     # gauss.gaussian_nll
                  optimizer = opt,
                  metrics = ['accuracy'])


    model.fit(i, o, batch_size = 2,  epochs = 1000)

