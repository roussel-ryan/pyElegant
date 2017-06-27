# -*- coding: utf-8 -*-
import logging

class AcceleratorElement(object):
	"""Generalized accelerator element
	
	Attributes:
		name: Name of element
		type: Type of element
	"""
	
	def __init__(self,name,type):
		self.name = name
		self.type = type

class BeamlineElement(AcceleratorElement):
	"""Single Beamline element -- QUAD,SBEN,etc.
	
	Attributes:
		name: Name of element
		type: Type of element
		parameters: Dict listing the parameters for the element
	"""
	def __init__(self,name,type,parameters):
		AcceleratorElement.__init__(self,name,type)
		if isinstance(parameters,dict):
			self.parameters = parameters
		else:
			raise RuntimeError('Input parameters are not a dict!' )
	
	def lattice_file_string(self):
		retString = [''.join(['{}: '.format(self.name).ljust(15),self.type,','])]
		for name,value in self.parameters.items():
			retString.append(''.join([name,'=',str(value),',']))
		#retString.append('\n')
		return ''.join(retString)[:-1]
	
class Beamline(AcceleratorElement):
	"""Beamline object
	
	Attributes:
		name: Name of element
		type: LINE element
		beamline_elements: 
	"""
	def __init__(self,name,element_list=[]):
		AcceleratorElement.__init__(self,name,'LINE')
		self.beamline_elements = element_list
		if self.check_for_sub_beamlines(self.beamline_elements):
			self.is_zipped = True
		else:
			self.is_zipped = False
	
	def check_for_sub_beamlines(self,element_list):
		for element in element_list:
			if isinstance(element,Beamline):
				return True
		return False
	
	def modify_element(self,old_element_name,new_element,old_element_index=0):
		""" find and replace element with name <old_element_name> with <new_element>"""
		try:
			found_indicies = self.get_element_index(old_element_name)
			self.beamline_elements[found_indicies[old_element_index]] = new_element
		except IndexError:
			logging.warning('Beamline element {} not found in beamline {}'.format(old_element_name,self.name))
	
	def get_element(self,element_name):
		"""Finds and returns the first BeamlineElement with the name element_name"""
		for ele in self.beamline_elements:
			if ele.name == element_name:
				return ele
				
	def get_element_index(self,element_name):
		"""Finds and returns all the indices of the BeamlineElement with the name element_name"""
		indices = []
		for index,ele in zip(range(0,len(self.beamline_elements)),self.beamline_elements):
			if ele.name == element_name:
				indices.append(index)
		return indices
	
	def get_sub_beamlines(self):
		"""get sub beamline objects in beamline"""
		sub_beamlines = []
		for element in self.beamline_elements:
			if isinstance(element,Beamline):
				sub_beamlines.append(element)
		return sub_beamlines
	
	def print_element_names(self):
		return ''.join([''.join([element.name,',']) for element in self.beamline_elements])
	
	def lattice_file_string(self):
		ret_string = ['{}: '.format(self.name).ljust(15),self.type,'=(']
		i=1
		#logging.debug([x.name for x in self.line])
		for ele in self.beamline_elements:
			if i % 10 == 0:
				ret_string.append('&\n\t\t\t')
			ret_string.append(''.join([ele.name,',']))
			i += 1
		ret_string.append(')')
		return ''.join(ret_string)
	
	def unzip(self):
		""" Search for sub bealines recusrively and expand them into sub componenets"""
		tmp_beamline = self.beamline_elements
		while True:
			is_zipped = self.check_for_sub_beamlines(tmp_beamline)
			if not is_zipped:
				break
			else:
				tmp_beamline = []
				for element in self.beamline_elements:
					if isinstance(element,Beamline):
						for ele in element.beamline_elements:
							tmp_beamline.append(ele)
					else:
						tmp_beamline.append(element)						
		return tmp_beamline
		
