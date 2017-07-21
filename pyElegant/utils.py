from subprocess import Popen, PIPE
import numpy as np
import logging
import sdds


def run_elegant(filename):
	process = Popen('elegant ' + filename)
	out,err = process.communicate()
	exit_code = process.wait()

def run_sdds_toolkit(cmd):
	process = Popen(cmd)
	out,err = process.communicate()
	exit_code = process.wait()

def read_sdds_file(filename,include_definitions=False):
	""" create and return dicts for the columns and the paramters"""
	data_file = sdds.SDDS(0)
	data_file.load(filename)
	
	parameters = {}
	parameter_def = {}
	for name,item in zip(data_file.parameterName,data_file.parameterData):
		if len(item)==1:
			parameters[name] = item[0]
		else:
			parameters[name] = item
		
	
	for name,item in zip(data_file.parameterName,data_file.parameterDefinition):
		parameter_def[name] = item
	
	columns = {}
	column_def = {}
	for name,item in zip(data_file.columnName,data_file.columnData):
		if len(item)==1:
			columns[name] = item[0]
		else:
			columns[name] = item
	
	for name,item in zip(data_file.columnName,data_file.columnDefinition):
		column_def[name] = item
	
	if include_definitions:
		return parameters,parameter_def,columns,column_def
	else:
		return parameters,columns
		
def gpt_screen_to_sdds(data=None, gpt_filename=None, sdds_filename = 'gpt_out.sdds'):
	if gpt_filename:
		#input an gpt screen file from gdf2a
		with open(gpt_filename) as f:
			data = []
			f.readline()
			#data_col_names = [x.split('(')[0] for x in f.readline().strip().split(' ') if not x=='']
			i=0
			for line in f:
				data.append([x for x in line.strip().split(' ') if not x==''])
				data[-1].append(i)
				i+=1
			n_data = np.asfarray(data).T
	
	if data:
		n_data = data
	
	data_col_names = ['x','y','t','xp','yp','p','particleID']
	sdds_file = sdds.SDDS(0)
	
	col_def = {'x':['','m','','',sdds_file.SDDS_DOUBLE,0],\
		'xp':['x\'','','','',sdds_file.SDDS_DOUBLE,0],\
		'y':['','m','','',sdds_file.SDDS_DOUBLE,0],\
		'yp':['y\'','','','',sdds_file.SDDS_DOUBLE,0],\
		't':['','s','','',sdds_file.SDDS_DOUBLE,0],\
		'p':['','m$be$nc','','',sdds_file.SDDS_DOUBLE,0],\
		'particleID':['','','','',sdds_file.SDDS_LONG,0]}
	
	for name,col in zip(data_col_names,n_data):
		sdds_file.defineColumn(name,*col_def[name])
		sdds_file.setColumnValueList(name,col.tolist(),1)
	if sdds_filename:
		sdds_file.save(sdds_filename)
	else:
		sdds_file.save(gpt_filename.split('.')[0] + '.sdds')
	return n_data