#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python predict.py [mileage]

Return estimated price\033[0m
"""

import sys
import os
import pandas as pd

def predict(mileage):
	try:
		miles = float(mileage)
	except ValueError:
		print("Please input a number")
		exit(42)
	if miles < 0:
		print("Only positive numbers")
		exit(42)

	# Retrieval of params
	#theta = getTheta()
	fileContent = getTheta()
	theta = fileContent[0]
	path = fileContent[1]
	if os.path.isfile(path):
		try:
			data = pd.read_csv(path, dtype={'km':float, 'price':float})
			kmMin = data.km.min()
			kmMax = data.km.max()
		except Exception as e:
			exit(e)
	else:
		kmMin = 0
		kmMax = 1

	return (theta[0] + (miles - kmMin) / (kmMax - kmMin) * theta[1])

def getTheta():
	if os.path.isfile('theta'):
		with open('theta', 'r') as f:
			theta0 = float(f.readline())
			theta1 = float(f.readline())
			path = f.readline()
		f.closed
	else:
		theta0 = 0.0
		theta1 = 0.0
		path = ""
	return [(theta0, theta1), path]

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		print("For %s km, estimated car price is %g." % (sys.argv[-1], predict(sys.argv[-1])))
