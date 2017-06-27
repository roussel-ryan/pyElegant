# -*- coding: utf-8 -*-
import sys
import numpy as np
import logging

import sdds
from pyElegant.beamline.mask import eex
from PrintVars import PrintVars

#masking script for use in elegant masking element

def main(input_filename,mask_config_filename):
	
	#import particle data in from file
	data_file = sdds.SDDS(0)
	output_file = sdds.SDDS(1)
	data_file.load(input_filename)
	
	
	PrintVars(locals())
	
	#apply masking
	logging.info('Applying masking')
	data = np.asarray([ele[0] for ele in data_file.columnData]).T
	result = eex.apply_mask(data,mask_config_filename).T
	
	#add an extra layer of brackets to result for pages
	paged_result = [[col.tolist()] for col in result]
	
	#write resulting bunch to new file with same name but .out ext
	logging.info('Setting up new file')
	for ele in data_file.description:
		output_file.description.append(ele)
	
	output_file.parameterName = data_file.parameterName
	output_file.parameterDefinition = data_file.parameterDefinition
	output_file.parameterData = data_file.parameterData
	
	output_file.columnName = data_file.columnName
	output_file.columnDefinition = data_file.columnDefinition
	output_file.columnData = paged_result
	
	logging.info('Writing to file')
	if '.in' in input_filename:
		output_file.save(input_filename.replace('.in','.out'))
	else:
		output_file.save(input_filename.split('.') + '.new')
	logging.info('Done writing to file')	
	del data_file
	del output_file

	
	
if __name__=='__main__':
	args = sys.argv
	mask_config_filename = 'default_linear.config'
	main(args[1],mask_config_filename)
	