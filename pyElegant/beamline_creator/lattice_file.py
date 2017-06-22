# -*- coding: utf-8 -*-
import logging
import re
import time

from . import accelerator
from ..analysis import rpn
""" Class for reading and writing lattice files"""


class LatticeFile:
	""" Class for reading and writing lattice files
	
	Attributes:
		filename: filename
		mode: similar to regular python read/write modes, changes permissions for overwriting files
			Modes:
				'r': read file, no overwriting allowed
				'w': write file truncating the file if it already exists
				'rw': read file and write to file truncating the file if it already exists
	"""
	READ = 0
	WRITE = 1
	READ_WRITE = 2
	mode_dict = {'r':READ,'w':WRITE,'rw':READ_WRITE}

	def __init__(self,filename,mode='r'):
		self.filename = filename
		self.mode = mode
		
		if not self.mode in self.mode_dict:
			raise RuntimeError('LatticeFile read/write mode not found!')
	
	def read(self):
		""" Read lattice file to find elements and beamlines and return beamline objects 
		filled with elements
		"""
		
		with open(self.filename,'r') as f:
			beamline_text = []
			elements = {}
			element_text = []
			divided_file_text = []
			tmp=[]
			for line in f:
				#check if the line is commented out
				if not '!' in line:
					#if not commented out add the line to the entry
					tmp.append(line)
					if not '&' in line:
						#if there is no & then cut it off and append
						divided_file_text.append(''.join(tmp))
						tmp = []
			
			#sanatize data inputs
			clean_text = []
			for ele in divided_file_text:
				text = ele.replace('\n','').replace('&','')
				#get rid of spaces outside quotes
				lst = text.split('"')
				for i, item in enumerate(lst):
					if not i % 2:
						lst[i] = re.sub('\s+', '', item).upper()
					else:
						#if inside quotes, use rpn calculator
						lst[i] = str(rpn.rpn(item))
				text = ''.join(lst)
				
				if not text=='':
					clean_text.append(text)
			#logging.debug(clean_text)
			
			#sort the entries into beamlines or elements based on 'LINE' keyword
			#elements must be defined before beamlines
			for entry in clean_text:
				if 'LINE' in entry.split(':')[1]:
					beamline_text.append(entry)
				else:
					element_text.append(entry)
			
			#add elements to list for searching 
			for entry in element_text:
				element_name = entry.split(':')[0]
				element_type = entry.split(':')[1].split(',')[0]
				element_params = entry.split(':')[1].split(',')[1:]
				element_params_dict = {}
				for param in element_params:
					splitParam = param.split('=')
					try:
						element_params_dict.update({splitParam[0]:float(splitParam[1])})
					except ValueError:
						element_params_dict.update({splitParam[0]:splitParam[1]})
				element = accelerator.BeamlineElement(element_name,element_type,element_params_dict)
				elements.update({element_name:element})
			
			for entry in beamline_text:
				beamline_name = entry.split(':')[0]
				beamline_elements = entry.split(':')[1].replace('LINE=(','').replace(')','').split(',')
				tmpBeamline = []
				for element in beamline_elements:
					tmpBeamline.append(elements[element])
				elements.update({beamline_name:accelerator.Beamline(beamline_name,tmpBeamline)})
			
			return elements
			
	def write(self,beamlines):
		""" Write the lattice file of a particular beamline with all dependant elements"""
		if self.mode_dict[self.mode] == self.READ:
			return None
		write_string = []
		
		lines=[]
		if isinstance(beamlines,list):
			n_beamlines = len(beamlines)
			lines = beamlines
		else:
			n_beamlines = 1
			lines.append(beamlines)
		
		#expand list to inculde sub beamlines
		sub_lines = []
		for line in lines:
			for sub in line.get_sub_beamlines():
				sub_lines.append(sub)
		lines = sub_lines + lines
		
		#header
		time_string = time.asctime(time.localtime(time.time()))
		beamline_names = [''.join([line.name,',']) for line in lines]
		header = (
			'!-----------------------------------------------------\n'
			'!Filename: {filename}\n'
			'!Date: {date}\n'
			'!Beamlines: {beamlines}\n'
			'!Lattice file generated using pyElegant\n'
			'!-----------------------------------------------------\n'
			).format(filename=self.filename,date=time_string,beamlines=''.join(beamline_names))
		write_string.append(header)
		
		#get list of elements which need writing and sort them by type and then name
		all_elements = []
		for beamline in lines:
			line_elements = beamline.unzip()
			for element in line_elements:
				if not element in all_elements:
					all_elements.append(element)
		sorted_all_elements = sorted(all_elements,key=lambda element: (element.type,element.name))
		
		element_past = accelerator.BeamlineElement('','',{})
		for element in sorted_all_elements:
			if not element_past.type == element.type:
				write_string.append('\n! {}\n!-------------\n'.format(element.type))
			write_string.append(element.lattice_file_string())
			write_string.append('\n')
			element_past = element  
			
		write_string.append('\n! {}\n!-------------\n'.format('LINE'))
		
		for beamline in lines:
			write_string.append(beamline.lattice_file_string())
			write_string.append('\n')
		
		with open(self.filename,'w') as w:
			w.write(''.join(write_string))
