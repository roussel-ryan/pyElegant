import logging

def format(m):
	mString = '\n'
	for x in m:
		for y in x:
			mString+=('%2.2f' % y).ljust(7)
		mString += '\n'
	return mString

def read_file(filename,beamline=None):
	"""
		read_file(filename,beamline=None)
			Read a matrix output file from "matrix_output" elegant command
	"""
	f = open(filename)
	matrix = []
	elementMatrix = []
	beamlineMatrix = []
	
	#read until you hit "C:"
	for line in f:
		if "C:" in line:
			break
			
	#start reading matrix data, only read lines with R at the beginning
	tempArray = []
	i = 0
	for line in f:
		if line[0] == 'R':
			tempArray.append(line.split())
		else:
			matrix.append(tempArray)
			tempArray = []
	#clean up elements that are empty
	matrix = [x for x in matrix if not x==[]]
	#remove R's and sort into element matrix or beamline matrix
	i = 1
	#logging.debug(matrix)
	for ele in matrix:
		tMatrix = []
		for j in ele:
			tMatrix.append(j[1:])
		#logging.debug(tMatrix)
		
		if i % 2 == 0:
			elementMatrix.append(tMatrix)
		else:
			beamlineMatrix.append(tMatrix)
		i += 1
	elementMatrix = np.asfarray(elementMatrix)
	beamlineMatrix = np.asfarray(beamlineMatrix)
	
	#add matricies to a dict that corresponds
	if beamline:
		elementMatrixDict = []
		beamlineMatrixDict = []
		
		#remove elements who don't have a length specified
		lineWOZeroElements = []
		for ele in beamline.line:
			if 'L' in ele.params:
				lineWOZeroElements.append(ele)
		
		for element,matrix in zip(lineWOZeroElements,elementMatrix):
			elementMatrixDict.append([element.name,matrix])
		
		for element,matrix in zip(lineWOZeroElements,beamlineMatrix):
			beamlineMatrixDict.append([element.name,matrix])
		return elementMatrixDict,beamlineMatrixDict # not actually a dict!
	else:
		return elementMatrix,beamlineMatrix
