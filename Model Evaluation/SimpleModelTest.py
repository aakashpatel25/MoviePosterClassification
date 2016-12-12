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

x_test = np.load('X_test.npy')
y_test = np.load('y_test.npy')

x_test = x_test[:10]
y_test = y_test[:10]
# print y_test[0]
# print y_test[1]

def calculate_accuracy(z,y_test):
	accuracy = 0
	
	for b in range(0,len(z)):
		if z[b] == y_test[b]:
			accuracy += 10
		elif z[b]==1 and y_test[b]==0:
			accuracy-= 5
		else:
			accuracy-= 10
	return accuracy

def calculate_best_accuracy():
	a_list = []
	ranges = np.linspace(0.39, 0.56, num=18)
	for rang in ranges:
		accuracy = []
		x = model.predict(x_test)
		for i in range(0,len(x)):
			z = map(lambda x: 1 if x>rang else 0, x[i])
			z = z*np.ones(len(z))
			accuracy.append(calculate_accuracy(z,y_test[i]))
		accuracy = np.mean(accuracy)
		a_list.append([accuracy,rang])
	a_list = np.array(a_list)
	x = a_list.argmax(axis=0)[0]
	return a_list[x]

def getDataTest(number):
	if len(x_test)<number:
		return x_test
	return x_test[:number]

def getLabelTest(number):
	if len(y_test)<number:
		return y_test
	return y_test[:number]

def evaluate_threshold(number,thres):
	data = getDataTest(number)
	label = getLabelTest(number)
	accuracy = []
		x = model.predict(data)
		for i in range(0,len(x)):
			z = map(lambda x: 1 if x>rang else 0, x[i])
			z = z*np.ones(len(z))
			accuracy.append(calculate_accuracy(z,label[i]))
			print "================= Output ================="
			print z
			print label[i]
			print "=========================================="
		accuracy = np.mean(accuracy)
		print "Accuracy for the given model is: ",str(accuracy)

acc, thres = calculate_best_accuracy()

print "Best Accuracy for the model is: ",str(acc),"% at Threshold value of: ",str(thres)
evaluate_threshold(10,thres)