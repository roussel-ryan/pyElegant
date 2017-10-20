# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import logging

dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append('\\'.join(dir_path.split('\\')[:-2]))

from pyElegant import utils
from pyElegant.simulation.masks import mask
from PrintVars import PrintVars
import sdds


#masking script for use in elegant masking element

def main(input_filename,mask_config_filename):
	logger = logging.getLogger('masking')
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler('mask.log')
	fh.setLevel(logging.DEBUG)
	logger.addHandler(fh)

	#import particle data in from file
	input_params,input_param_def,input_columns,input_col_def = utils.read_sdds_file(input_filename,include_definitions=True)
	output_file = sdds.SDDS(1)

	PrintVars(locals())

	#apply masking
	data = np.asarray([item for name,item in input_columns.items()]).T
	logger.info('Applying masking with {} particles'.format(len(data)))

	#create mask
	mask_obj = mask.Mask(mask_config_filename)
	logger.debug(mask_obj.params)
	result = mask_obj.apply_mask(data).T

	logger.info('Done applying mask, {} particles transmitted'.format(len(result.T)))

	#add an extra layer of brackets to result for pages
	paged_result = [[col.tolist()] for col in result]

	#write resulting bunch to new file with same name but .out ext
	logger.info('Setting up new file')
	#for ele in data_file.description:
	#	output_file.description.append(ele)
	for name,item in input_params.items():
		output_file.parameterName.append(name)
		output_file.parameterDefinition.append(input_param_def[name])
		output_file.parameterData.append([item])

	for name,item in zip(input_columns.keys(),paged_result):
		output_file.columnName.append(name)
		output_file.columnDefinition.append(input_col_def[name])
		output_file.columnData.append(item)

	if '.in' in input_filename:
		logger.info('Writing to file {}'.format(input_filename.replace('.in','.out')))
		output_file.save(input_filename.replace('.in','.out'))
	else:
		logger.info('Writing to file {}'.format(input_filename.replace('.in','.out')))
		output_file.save(input_filename.split('.') + '.new')
	logger.info('Done writing to file')
	del output_file



if __name__=='__main__':
	args = sys.argv
	main(args[1],args[2])
