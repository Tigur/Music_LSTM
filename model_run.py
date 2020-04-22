TF_Api = True

if TF_Api :

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, LSTM, CuDNNLSTM
    import gaussian_nll as gauss
    from keras import losses

    from NN_preprocessing import new_preprocessing as prep
    import numpy as np
    import pdb
    import pprint as pp
else :
    import tensorflow as tf
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, LSTM, CuDNNLSTM
    from keras.optimizers import adam
    import gaussian_nll as gauss
    from keras import losses

    from NN_preprocessing import new_preprocessing as prep
    import numpy as np
    import pdb
    import pprint as pp

opt_CuDNN = False

rel_path = '/home/resolution/POważne_sprawy/studyjne/PRACA_INŻ/Inż_repo/MUSIC_PACKAGE/fav/'

scores = prep.loadScores(rel_path)
i ,o = prep.make_food(scores)

i = np.array(i)
o = np.array(o)

#pp.pprint(i)

#print(prep.check_tempo(scores[1]))

test = np.zeros((5,5))
#pp.pprint(test)
#print(i[1])

#THis is input shape probably.
#So how do I Feed it to keras .:PPP
i = np.reshape(i, (40,100,140))
o = np.reshape(o, (40,100,140))

in_sh = i.shape
if __name__ == "__main__":
    if opt_CuDNN:
        model = Sequential()
        model.add(CuDNNLSTM(70, input_shape=in_sh[1:],  return_sequences = True))
        model.add(Dropout(0.2))

        model.add(CuDNNLSTM(128,return_sequences=True))
        model.add(Dropout(0.2))

        model.add(CuDNNLSTM(128, return_sequences = True))
        model.add(Dropout(0.2))

        model.add(CuDNNLSTM(128, return_sequences = True))
        model.add(Dropout(0.2))

        model.add(Dense(140,activation = 'softmax')) # >>> odpowiada za ostatni shape.

        f_loss = losses.mean_squared_logarithmic_error

        if not TF_Api:
            opt = adam(lr=1e-3, decay=1e-6)
        if TF_Api:
            opt = tf.keras.optimizers.Adam(lr=1e-3, decay=1e-6)

        model.compile(loss=f_loss,     # gauss.gaussian_nll
                      optimizer = opt,
                      metrics = ['accuracy'])


        #pdb.set_trace()
        #model.fit_generator(batch_gen, epochs=3)
        #model.fit(i, o, batch_size = 10, epochs = 300)
        model.fit(i, o, batch_size = 2,  epochs = 300)
        #pdb.post_mortem()


    else:
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
        if not TF_Api:
            opt = adam(lr=1e-3, decay=1e-6)
        if TF_Api:
            opt = tf.keras.optimizers.Adam(lr=1e-4, decay=1e-6)

        model.compile(loss=f_loss,     # gauss.gaussian_nll
                      optimizer = opt,
                      metrics = ['accuracy'])


        #pdb.set_trace()
        #model.fit_generator(batch_gen, epochs=3)
        #model.fit(i, o, batch_size = 10, epochs = 300)
        model.fit(i, o, batch_size = 2,  epochs = 1000)
        #pdb.post_mortem()

