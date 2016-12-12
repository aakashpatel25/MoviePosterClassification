import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.callbacks import CSVLogger
import inception_v3 as inception
import os

N_CLASSES = 10
IMSIZE = (299, 299)

base_model = inception.InceptionV3(weights='imagenet')

for layer in base_model.layers:
    layer.trainable = False

x = Dense(32, activation='relu')(base_model.get_layer('flatten').output)
x = Dropout(0.5)(x)
predictions = Dense(N_CLASSES, activation='sigmoid', name='predictions')(x)

model = Model(input=base_model.input, output=predictions)

model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
model.save('Inception.h5')

x_train = np.load('X_train.npy')
y_train = np.load('Y_train.npy')
x_val = np.load('X_val.npy')
y_val = np.load('Y_val.npy')

x_train = x_train[:500]
y_train = y_train[:500]
x_val = x_val[:50]
y_val = y_val[:50]

csv_logger = CSVLogger('500TrainingExamples.csv',separator='\n', append=True)
model.fit(x_train,y_train,batch_size=25, nb_epoch=35,callbacks=[csv_logger],validation_data=(x_val,y_val))
model.save_weights('model_train.h5')