import numpy as np

def main(data):
	print('press enter to continue')
	input()
	nData = []
	for ele in data:
		if ele[0]**2 + ele[2]**2 < 0.05**2:
			nData.append(ele)
	return np.asfarray(nData)
