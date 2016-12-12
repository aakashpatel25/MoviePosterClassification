from PIL import Image
import pandas as pd
import numpy as np
import os

gen_size = 10
genre = ['action','drama','horror','comedy','romance','mystery','adventure','fantasy','sci-fi','animation']

movie_path = 'modified.csv'
image_path = 'Conv3/'

def hot_encode(gen):
	ls = np.zeros(gen_size)
	gen = gen.split('|')
	for g in gen:
		try:
			loc = genre.index(g.lower())
			ls[loc] = 1
		except:
			pass
	return ls

def load_image(infilename):
    img = Image.open(infilename)
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def read_files():
	files = os.listdir(image_path)
	final_data = []
	for file in files:
		try:
			datapoint = []
			feature = load_image(image_path+file)
			feature = feature.astype("float32")
			feature /= 255
			feature = np.expand_dims(feature, axis=0)
			mvid = file.split('.')[0]
			movie = movie_data[movie_data.index==mvid]['Genre']
			genre = movie[mvid]
			gen = hot_encode(genre)
			#gen = np.expand_dims(gen, axis=0)
			datapoint = [feature,gen]
			final_data.append(datapoint)
		except:
			pass
	return final_data

movie_data = pd.read_csv(movie_path,index_col='MovieID')
data = read_files()
np.random.seed(seed=26)
np.random.shuffle(data)
count = len(data)

train = int((count/100.0)*60.0)
val = int((count/100.0)*25.0)

print train
print val



train_set = data[0:train]
val_set = data[train:train+val]
test_set = data[train+val:]

train_set = np.array(train_set)
val_set = np.array(val_set)
test_set = np.array(test_set)


X_train = train_set[:,0]
Y_train = train_set[:,1]

X_val = val_set[:,0]
Y_val = val_set[:,1]

X_test = test_set[:,0]
Y_test = test_set[:,1]

feat = X_train[0]
lab = [Y_train[0]]

len_train = len(X_train)
print 'Converting Train Set ...'
for i in range(1,len_train):
	try:
		print 'Doing Training ',str(i),' of ',str(len_train),'.......'
		feat = np.vstack((feat,X_train[i]))
		lab.append(Y_train[i])
	except:
		print "======================> Error in train set"
		continue
print 'Finished Converting Train Set ...'

lab = np.array(lab)
np.save('X_train',feat)
np.save('Y_train',lab)

feat_val = X_val[0]
lab_val = [Y_val[0]]

len_val = len(X_val)
print 'Converting Validation Set ...'
for i in range(1,len_val):
	try:
		print 'Doing Validation ',str(i),' of ',str(len_val),'......'
		feat_val = np.vstack((feat_val,X_val[i]))
		lab_val.append(Y_val[i])
	except:
		print "======================> Error in val set"
		continue
print 'Finished Converting Validation Set ...'

lab_val = np.array(lab_val)
np.save('X_val',feat_val)
np.save('Y_val',lab_val)

feat_test = X_test[0]
lab_test = [Y_test[0]]

print 'Converting Test Set ...'
len_test = len(X_test)
for i in range(1,len_test):
	try:
		print 'Doing Test ',str(i),' of ',str(len_test),'....'
		feat_test = np.vstack((feat_test,X_test[i]))
		lab_test.append(Y_test[i])
	except:
		print "================> Error in test set"
		continue
print 'Finished Converting Test Set ...'

lab_test = np.array(lab_test)
np.save('X_test',feat_test)
np.save('Y_test',lab_test)
