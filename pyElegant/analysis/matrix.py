import logging
import numpy as np

from pyElegant import utils

def format(m):
	'''
		format(m)
			formats output from matrix.read_file

		returns mString
			fomatted string for printing

	'''
	mString = '\n'
	for x in m:
		for y in x:
			mString+=('%2.2f' % y).ljust(7)
		mString += '\n'
	return mString

def read_mat_file(filename):
	"""
		read_mat_file(filename)
			Read a .mat file to get matricies

		returns matrix,beamline_elements
			- matrix = matrix of entire beamline up to element ref by element number
	"""
	params,cols = utils.read_sdds_file(filename)
	matrix = []
	for i in range(0,len(cols['ElementName'])):
		matrix.append(np.asfarray(\
			[[cols['R11'][i],cols['R12'][i],cols['R13'][i],cols['R14'][i],cols['R15'][i],cols['R16'][i]],\
			[cols['R21'][i],cols['R22'][i],cols['R23'][i],cols['R24'][i],cols['R25'][i],cols['R26'][i]],\
			[cols['R31'][i],cols['R32'][i],cols['R33'][i],cols['R34'][i],cols['R35'][i],cols['R36'][i]],\
			[cols['R41'][i],cols['R42'][i],cols['R43'][i],cols['R44'][i],cols['R45'][i],cols['R46'][i]],\
			[cols['R51'][i],cols['R52'][i],cols['R53'][i],cols['R54'][i],cols['R55'][i],cols['R56'][i]],\
			[cols['R61'][i],cols['R62'][i],cols['R63'][i],cols['R64'][i],cols['R65'][i],cols['R66'][i]]]
		))
	return matrix

def get_element_indices(element_name,beamline_element_list):
	return [i for i, x in enumerate(beamline_element_list) if x == element_name]

def get_element_matrix(matrix_col,element_index):
	"""
		get_element_matrix(filename,element_name,previous_element)
			Read a .mat file to get matricies
			- matrix_col = output column returned from matrix.read_mat_file
			- element_index = element index for which the matrix will be returned

		returns element_matrix
			- element_matrix = matrix of ref'd element
	"""
	if element_index > 0:
		return get_point_to_point_matrix(matrix_col,element_index-1,element_index)
	else:
		return matrix_col[0]

def get_point_to_point_matrix(matrix_col,upstream_index,downstream_index):
	"""
		get_point_to_point_matrix(filename,upstream_index,downstream_index)
			Read a .mat file to get matricies
			- matrix_col = output column returned from matrix.read_mat_file
			- upstream_index = first element index
			- downstream_index = last element index

		returns element_matrix
			- element_matrix = resulting matrix
	"""
	return np.dot(np.asfarray(matrix_col[downstream_index]),np.linalg.inv(np.asfarray(matrix_col[upstream_index])))

def read_file(filename,beamline=None):
	"""
		read_file(filename,beamline=None)
			Read a matrix output file from "matrix_output" elegant command

		returns elementMatrix, beamlineMatrix
			- elementMatrix = matrix of particular element ref by name if <beamline> is specified or element number otherwise
			- beamlineMatrix = matrix of entire beamline up to element ref by name if <beamline> is specified or element number otherwise
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
