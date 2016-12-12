import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.callbacks import CSVLogger
from keras.models import load_model
import inception_v3 as inception
import os

N_CLASSES = 10
IMSIZE = (299, 299)

model = load_model('Inception.h5')
model.load_weights('model_train.h5')

train = np.load('train.npy')
val = np.load('val.npy')
test = np.load('test.npy')



csv_logger = CSVLogger('training.csv',separator='\n', append=True)
model.fit(feat,lab,batch_size=24, nb_epoch=3,callbacks=[csv_logger],validation_data=(feat_val,lab_val))
model.save('Inception.h5')
model.save_weights('model_train.h5')