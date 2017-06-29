from subprocess import Popen, PIPE
import sdds


def run_elegant(filename):
	process = Popen('elegant ' + filename)
	out,err = process.communicate()
	exit_code = process.wait()
	
def read_SDDS_file(filename,include_definitions=False):
	""" create and return dicts for the columns and the paramters"""
	data_file = sdds.SDDS(0)
	data_file.load(filename)
	
	parameters = {}
	parameter_def = {}
	for name,item in zip(data_file.parameterName,data_file.parameterData):
		parameters[name] = item
	
	for name,item in zip(data_file.parameterName,data_file.parameterDefinition):
		parameter_def[name] = item
	
	columns = {}
	column_def = {}
	for name,item in zip(data_file.columnName,data_file.columnData):
		columns[name] = item
	
	for name,item in zip(data_file.columnName,data_file.columnDefinition):
		column_def[name] = item
	
	if include_definitions:
		return parameters,parameter_def,columns,column_def
	else:
		return parameters,columns