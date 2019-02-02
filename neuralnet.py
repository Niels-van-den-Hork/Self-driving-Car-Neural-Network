import argparse

import numpy as np
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPRegressor,MLPClassifier
from sklearn.model_selection import train_test_split

import utils

def abs(x):
	if x > 0:
		return x
	return -x

def train():
	# train
	print("Training the network, please wait a few seconds")
	nn_power.fit(input_train,output_train[:,0])
	nn_steer.fit(input_train,output_train[:,1])

def test():
	# test
	output_power_pred = nn_power.predict(input_test)
	output_steer_pred = nn_steer.predict(input_test)

	# evaluate test data
	count = 0
	for i in range(len(output_test[:,0])):
		if abs(output_power_pred[i] - output_test[i,0]) < 0.5 :
			count += 1

	print("power: "+str(count/len(output_test)))

	count = 0
	for i in range(len(output_test[:,1])):
		if abs(output_steer_pred[i] - output_test[i,1]) < 0.5:
			count += 1

	print("steer: "+ str(count/len(output_test)))

def predict(input):
	power = nn_power.predict([input])[0]
	steer = nn_steer.predict([input])[0]
	print(power,steer,input)
	return power,steer



parser = argparse.ArgumentParser(description='Neural Network interface')
parser.add_argument('-l','--hidden_layers',type=int,default=10)
parser.add_argument('-r','--random',type=int,default=5)

args = parser.parse_args()
hidden_layers = args.hidden_layers
random = args.random


# load data
inputs,outputs = utils.load_training("tdata")
inputs = np.array(inputs,dtype=np.float64)
outputs = np.array(outputs,dtype=np.float64)

# split and randomise data
input_train,input_test,output_train,output_test = train_test_split(inputs,outputs,test_size=0.05,random_state=random)


# init neural net
nn_power = MLPClassifier(hidden_layer_sizes=(hidden_layers,hidden_layers),random_state=random,activation='tanh')
nn_steer = MLPClassifier(hidden_layer_sizes=(hidden_layers,hidden_layers),random_state=random,activation='tanh')

train()
print("training complete")
test()
print("testing complete")

