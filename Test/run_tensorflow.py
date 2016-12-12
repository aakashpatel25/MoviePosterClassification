import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.callbacks import CSVLogger
from keras.models import load_model
import os

N_CLASSES = 10
IMSIZE = (299, 299)

model = load_model('Inception.h5')
model.load_weights('model_train.h5')

x_test = np.load('test.npy')

x = model.predict(x_test)
x = x[0]
x = [str(ele) for ele in x]
x = "|".join(x)
print x

with open("output.txt", "w") as text_file:
    text_file.write(x)