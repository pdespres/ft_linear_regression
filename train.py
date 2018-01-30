#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python train.py [-s] [path to the data file]

Supported options:
	-s 		silent		don't show the messages
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt 
import predict

# Find the min and max values for each column
def dataset_minmax(dataset):
	minmax = list()
	for i in range(len(dataset[0])):
		col_values = [row[i] for row in dataset]
		value_min = min(col_values)
		value_max = max(col_values)
		minmax.append([value_min, value_max])
	return minmax

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
	for row in dataset:
		for i in range(len(row)):
			row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

# Calculate root mean squared error
def rmse_metric(actual, predicted):
	sum_error = 0.0
	for i in range(len(actual)):
		prediction_error = predicted[i] - actual[i]
		sum_error += (prediction_error ** 2)
	mean_error = sum_error / float(len(actual))
	return mean_error**0.5

def train(path, verbose=True):
	# modable params
	l_rate = 0.01
	n_epoch = 100

	data = pd.read_csv('./data.csv')
	print data
	data.plot(kind='scatter', x='km', y='price', figsize=(16, 8))
	#plt.show()
	print("Baseline Performance ZeroR: mean %g  RootMeanSquareError(RMSE) %g" % (data["price"].mean(), 
		rmse_metric(data["price"], [data["price"].mean() for i in xrange(24)])))
	# normalize
	#print(data[0])
	#print(len(data[0]))
	#minmax = dataset_minmax(data)
	#normalize_dataset(data, minmax)

	for epoch in range(n_epoch):
		for row in data:
			print(row)
			yhat = predict(row, coef)
			error = yhat - row[-1]
			coef[0] = coef[0] - l_rate * error
			for i in range(len(row)-1):
				coef[i + 1] = coef[i + 1] - l_rate * error * row[i]
			print(l_rate, n_epoch, error)

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 4):
		print(__doc__)
	elif argc == 3:
		#traitement params
		param = 0
		if (sys.argv[1][0] == '-' and len(sys.argv[1]) in range(2,3)):
			if sys.argv[1].find('s') > 0:
				train(sys.argv[-1], False)
			else:
				print(__doc__)
		else:
			print(__doc__)
	else:
		train(sys.argv[-1])