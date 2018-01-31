#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python predict.py [mileage]

Return estimated price\033[0m
"""

import sys
import os

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
	theta = getTheta()

	return (theta[0] + (miles - 22899) / (240000 - 22899) * theta[1])

def getTheta():
	if os.path.isfile('theta'):
		with open('theta', 'r') as f:
			theta0 = float(f.readline())
			theta1 = float(f.readline())
		f.closed
	else:
		theta0 = 0.0
		theta1 = 0.0
	return (theta0, theta1)

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		print("For %s km, estimated car price is %g." % (sys.argv[-1], predict(sys.argv[-1])))
