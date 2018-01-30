#!/usr/bin/env python 2.7
# waloo le encoding: utf-8 de malade

"""
\033[32musage:	python predict.py [mileage]

Return estimated price
"""

def predict(mileage):
	if mileage < 0:
		print("Only positivie numbers")
		exit(42)
	
	return price

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc not in range(2, 3):
		print(__doc__)
	else:
		print(predict(sys.argv[-1]))