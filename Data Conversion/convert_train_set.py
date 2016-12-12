from PIL import Image
import pandas as pd
import numpy as np
import os

gen_size = 10
genre = ['action','drama','horror','comedy','romance','mystery','adventure','fantasy','sci-fi','animation']

movie_path = 'modified.csv'
image_path = 'color5k/'

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

X_train = data[:,0]
Y_train = data[:,1]

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