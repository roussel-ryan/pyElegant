#test python script for test PythonElement
def main(data):
	print('running\n\n\n\n\n\n')
	n_data = []
	for ele in data:
		if ele[0]**2 + ele[2]**2 < 0.05:
			n_data.append(ele)

	return []
