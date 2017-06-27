# -*- coding: utf-8 -*-
import sys
import os

from . import accelerator

class MaskElement(accelerator.BeamlineElement):
	def __init__(self,name,mask,keep_files = False):
		dir_path = os.path.dirname(os.path.abspath(__file__))
		script_filename = dir_path + '\\masking_script.py'
		
		if keep_files:
			kf = 1
		else:
			kf = 0
			
		params = {'COMMAND':' '.join(('\"python',script_filename,'%i\"')),'rootname':'\"mask\"',\
		'input_extension':'\"in\"',\
		'output_extension':'\"out\"',\
		'KEEP_FILES':str(kf),\
		'USE_CSH':'0'}
	
		accelerator.BeamlineElement.__init__(self,name,'SCRIPT',params)
		
		
if __name__=='__main__':
	test_element = MaskElement('test',None)
	print(test_element.parameters)