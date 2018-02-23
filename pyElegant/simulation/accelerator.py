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
			if isinstance(value,str):
				retString.append(''.join([name,'=','\"',value,'\"',',']))
			else:
				retString.append(''.join([name,'=',str(value),',']))
		#retString.append('\n')
		return ''.join(retString)[:-1]
		
	def get_length(self):
		try:
			return self.parameters['L']
		except KeyError:
			return 0.0
	
class Beamline(AcceleratorElement):
	"""Beamline object
	
	Attributes:
		name: Name of element
		type: LINE element
		elements: 
	"""
	def __init__(self,name,elements=[]):
		AcceleratorElement.__init__(self,name,'LINE')
		self.elements = elements
		self.element_coordinates = []
		if self.check_for_sub_beamlines(self.elements):
			self.is_zipped = True
			self._unzipped_elements = self.unzip()
		else:
			self.is_zipped = False
			self._unzipped_elements = self.elements
			
		self.calculate_element_coordinates()
	
	def check_for_sub_beamlines(self,element_list):
		for element in element_list:
			if isinstance(element,Beamline):
				return True
		return False
	
	def replace_element(self,old_element_name,new_element,old_element_index=0,replace_all=False):
		""" find and replace element with name <old_element_name> with <new_element>"""
		try:
			found_indicies = self.get_element_index(old_element_name)
			if replace_all:
				for ele in found_indicies:
					self.elements[ele] = new_element
			else:
				self.elements[found_indicies[old_element_index]] = new_element
		except IndexError:
			logging.warning('Beamline element {} not found in beamline {}'.format(old_element_name,self.name))
	
	def modify_element(self,element_name,params):
		""" find and alter the first found element of <element_name>"""
		try:
			self.get_element(element_name).parameters.update(params)
		except IndexError:
			logging.warning('Beamline element {} not found in beamline {}'.format(element_name,self.name))
	
	
	def get_element(self,element_name):
		"""Finds and returns the first BeamlineElement with the name element_name"""
		for ele in self.elements:
			if ele.name == element_name:
				return ele
		raise IndexError
				
	def get_element_index(self,element_name):
		"""Finds and returns all the indices of the BeamlineElement with the name element_name"""
		indices = []
		for index,ele in zip(range(0,len(self.elements)),self.elements):
			if ele.name == element_name:
				indices.append(index)
		return indices
	
	def get_sub_beamlines(self):
		"""get sub beamline objects in beamline"""
		sub_beamlines = []
		for element in self.elements:
			if isinstance(element,Beamline):
				sub_beamlines.append(element)
		return sub_beamlines
	
	def calculate_element_coordinates(self):
		pos = 0
		self.element_coordinates = [pos]
		for ele in self._unzipped_elements:
			pos += ele.get_length() 
			self.element_coordinates.append(pos)
	
	def print_element_names(self):
		return ''.join([''.join([element.name,',']) for element in self.elements])
	
	def lattice_file_string(self):
		ret_string = ['{}: '.format(self.name).ljust(15),self.type,'=(']
		i=1
		#logging.debug([x.name for x in self.line])
		for ele in self.elements:
			if i % 10 == 0:
				ret_string.append('&\n\t\t\t')
			ret_string.append(''.join([ele.name,',']))
			i += 1
		ret_string[-1] = ret_string[-1][:-1]
		ret_string.append(')')
		return ''.join(ret_string)
	
	def unzip(self):
		""" Search for sub bealines recusrively and expand them into sub componenets"""
		tmp_beamline = self.elements
		while True:
			is_zipped = self.check_for_sub_beamlines(tmp_beamline)
			if not is_zipped:
				break
			else:
				tmp_beamline = []
				for element in self.elements:
					if isinstance(element,Beamline):
						for ele in element.elements:
							tmp_beamline.append(ele)
					else:
						tmp_beamline.append(element)						
		return tmp_beamline
		
