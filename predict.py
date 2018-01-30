#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python predict.py [mileage]

Return estimated price
"""

def predict(mileage):
	if mileage(not number):
		print("Please input a number")
		exit(42)
	if mileage < 0:
		print("Only positive numbers")
		exit(42)
	if os.path.exists('theta.txt'):
        	with open('theta.txt') as f:
            		theta0 = float(f.readline())
            		theta1 = float(f.readline())
    	else:
        	theta0 = 0
        	theta1 = 0
		
	return (theta0 + mileage * theta1)

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		print("Estimated car price: %g" % predict(sys.argv[-1]))
