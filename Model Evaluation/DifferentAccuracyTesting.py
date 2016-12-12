import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.callbacks import CSVLogger
from keras.models import load_model
import os
import csv

N_CLASSES = 10
IMSIZE = (299, 299)

model = load_model('Inception.h5')
model.load_weights('model_train.h5')

x_test = np.load('X_test.npy')
y_test = np.load('y_test.npy')
movie_id = np.load('MovieID.npy')

# x_test = x_test[:1]
# y_test = y_test[:1]
# movie_id = movie_id[:1]
# print y_test[0]
# print y_test[1]

def calc_bias_accuracy(z,y_test):
	accuracy = 0
	
	for b in range(0,len(z)):
		if z[b] == y_test[b]:
			accuracy += 10
		elif z[b]==1 and y_test[b]==0:
			accuracy-= 5
		else:
			accuracy-= 10
	return accuracy

def calculate_accuracy(z,y_test):
	accuracy = 0
	count = 0
	for b in range(0,len(z)):
		if z[b] == y_test[b] and y_test[b]==1:
			accuracy += 1
			count+= 1
		elif z[b] == y_test[b] and y_test[b]==0:
			pass
		else:
			count+= 1
	return accuracy/float(count)

def strict_acc(z,y_test):
	for b in range(0,len(z)):
		if z[b] != y_test[b]:
			return 0
	return 100

def calculate_best_accuracy():
	a_list = []
	ranges = np.linspace(0.39, 0.56, num=18)
	for rang in ranges:
		print 'Evaluating Accuracy for i = %s' % str(rang)
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

def getMovieTitle(number):
	if len(movie_id)<number:
		return movie_id
	return movie_id[:number]

def full_acc(number,thres):
	data = getDataTest(number)
	label = getLabelTest(number)
	accuracy = []
	x = model.predict(data)
	for i in range(0,len(x)):
		z = map(lambda x: 1 if x>thres else 0, x[i])
		z = z*np.ones(len(z))
		accuracy.append(strict_acc(z,label[i]))
		# print "================= Output ================="
		# print z
		# print label[i]
		# print "=========================================="
	accuracy = np.mean(accuracy)
	print "Accuracy for the given model is: ",str(accuracy)

def evaluate_threshold(number,thres):
	data = getDataTest(number)
	label = getLabelTest(number)
	accuracy = []
	x = model.predict(data)
	for i in range(0,len(x)):
		z = map(lambda x: 1 if x>thres else 0, x[i])
		z = z*np.ones(len(z))
		accuracy.append(calculate_accuracy(z,label[i]))
		# print "================= Output ================="
		# print z
		# print label[i]
		# print "=========================================="
	accuracy = np.mean(accuracy)
	print "Accuracy for the given model is: ",str(accuracy)


def save_output(number):
	data = getDataTest(number)
	label = getLabelTest(number)
	#accuracy = []
	out = []
	x = model.predict(data)
	for i in range(0,len(x)):
		#z = map(lambda x: 1 if x>thres else 0, x[i])
		z = x[i]
		z = [str(ele) for ele in z]
		lab = [str(int(ele)) for ele in label[i]]
		out.append(['|'.join(z),'|'.join(lab),movie_id[i]])
	with open("output.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(out)
		# print "================= Output ================="
		# print z
		# print label[i]
		# print "=========================================="
	#accuracy = np.mean(accuracy)
	#print "Accuracy for the given model is: ",str(accuracy)

#acc, thres = calculate_best_accuracy()

#print "Best Accuracy for the model is: ",str(acc),"% at Threshold value of: ",str(thres)
#evaluate_threshold(1,0.49)
#full_acc(1,0.49)

save_output(1000)