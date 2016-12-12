import numpy as np
import subprocess
from PIL import Image
import os

def load_image(infilename):
	img = Image.open(infilename)
	img.load()
	data = np.asarray(img, dtype="float32" )
	return data

def read_files(path):
	feature = load_image(str(path))
	feature /= 255
	feature = np.expand_dims(feature, axis=0)
	np.save('test',feature)

def return_label(path):
	read_files(path)
	print 'Image generation complete.....'
	process = subprocess.Popen(['./script.sh'], shell=True, stdout=subprocess.PIPE)
	process.wait()
	print 'Subprocess complete.....'
	file = open('output.txt', 'r')
	x = file.read()
	file.close()
	return x