#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python train.py [-s] [path to the data file]

Supported options:
	-s 		silent		don't show the messages\033[0m
"""

import sys
import os
import warnings
import subprocess
import pandas as pd
import matplotlib.pyplot as plt 
import predict

warnings.simplefilter(action='ignore', category=FutureWarning)

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
	#return round(mean_error**0.5,4)
	return mean_error**0.5

def train(path, verbose=True):
	if os.path.isfile(path):
		try:
			data = pd.read_csv(path, dtype={'km':float, 'price':float})
		except Exception as e:
			exit(e)
	else:
		print("No file found. Please check your data file path.")
		sys.exit(42)
			  
	# modable params
	l_rate = 0.1

	# init. plot dataset + calculate benchmark basis (ZeroR)
	if verbose:
		print("Dataset:")
		print data
	data.plot(kind='scatter', x='km', y='price', figsize=(16, 8))
	plt.savefig('dataset.png')

	# Normalize. Rescale dataset columns to the range 0-1
	kmMin = data.km.min()
	kmMax = data.km.max()
	for index, row in enumerate(data.km):
		data.km[index] = (row - kmMin) / (kmMax - kmMin)
	#pMin = data.price.min()
	#pMax = data.price.max()
	#for index, row in enumerate(data.price):
	#	data.price[index] = (row - pMin) / (pMax - pMin)

	rmse = rmse_metric(data.price, [data.price.mean() for i in xrange(24)])
	if verbose:
		#subprocess.call(['open', 'dataset.png'])
		print("\033[32mBaseline Performance (ZeroR):")
		print("Mean %g  RootMeanSquareError(RMSE) %g\033[0m" % (data.price.mean(), rmse))

	# gradient descent for 'epoch' iterations
	converged = False
	epoch = 0
	rmse = 0
	while not converged:
		epoch += 1
		fileContent = predict.getTheta()
		theta = fileContent[0]
		gradient0 = 0
		gradient1 = 0
		priceTemp = []
		n = float(len(data.km))
		for index, miles in enumerate(data.km):
			pprice = theta[0] + theta[1] * miles
			priceTemp.append(pprice)
			gradient0 += (pprice - data.price[index])
			gradient1 += (pprice - data.price[index]) * miles
		t0 = theta[0] - l_rate * gradient0 / n
		t1 = theta[1] - l_rate * gradient1 / n
		temp = rmse_metric(data.price, priceTemp)
		if rmse != 0 and temp >= rmse:
			converged = True
			print("\033[32mConvergence achieved at epoch %g\033[0m" % (epoch - 1))
		else:
			rmse = temp
			if verbose:
				if epoch < 11 or (epoch < 300 and epoch % 50 == 0) or (epoch % 100 == 0):
					print("Epoch %g: thetas (0, 1) (%g, %g)  RMSE %g" % (epoch, t0, t1, rmse))

			# save results
			with open('theta', 'w') as f:
				f.write(str(t0))
				f.write("\n")
				f.write(str(t1))
				f.write("\n")
				f.write(path)

			if epoch > 5000:
				converged = True
				print("Epoch > 5000. Failure.")

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
