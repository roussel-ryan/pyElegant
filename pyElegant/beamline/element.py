# -*- coding: utf-8 -*-
import sys
import os

class BeamlineElement:
	def __init__(self,name,type,parameters):
		self.name = name
		self.type = type
		self.parameters = parameters
	
	def writeElement(self):
		retString = self.name + ': ' + self.type + ','
		for name,value in self.params.items():
			retString += name + '=' + str(value) + ','
		retString = retString[:-1] + '\n'
		return retString
		
class MaskElement(BeamlineElement):
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
	
		BeamlineElement.__init__(self,name,'SCRIPT',params)
		
		
if __name__=='__main__':
	test_element = MaskElement('test',None)
	print(test_element.parameters)