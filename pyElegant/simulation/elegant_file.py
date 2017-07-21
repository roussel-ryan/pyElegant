# -*- coding: utf-8 -*-
import logging
import re
import time
import copy

from collections import OrderedDict

from . import accelerator
from ..analysis import rpn

""" Class for reading and writing elegant files"""
class ElegantFile:
	""" Class for reading and writing elegant main files
	
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
		""" Read main file to find args
		"""
		with open(self.filename,'r') as f:
			lines = []
			for line in f:
				if not '!' in line:
					lines.append(line.rstrip().replace(' ','').replace('\t','').split(','))
		args_list = [x for y in lines for x in y if not x=='']
		
		self.commands = []

		curr_command = None
		while len(args_list):
			arg = args_list.pop(0)
			if '&' in arg:
				if '&end' == arg:
					self.commands.append(curr_command)
					del(curr_command)
				else:
					curr_command = Command(arg[1:],{})
			else:
				curr_command.args[arg.split('=')[0]] = arg.split('=')[1]
			#try:
				#logging.debug(curr_command.name)	
				#logging.debug(curr_command.args)
			#except UnboundLocalError:
			#	pass
			
		return self.commands
			
	def write(self,commands):
		""" Write the elegant file with dict commands"""
		if self.mode_dict[self.mode] == self.READ:
			logging.error('File is read-only!')
			return None
		write_string = []
		
		#header
		time_string = time.asctime(time.localtime(time.time()))
		header = (
			'!-----------------------------------------------------\n'
			'!Filename: {filename}\n'
			'!Date: {date}\n'
			'!Elegant file generated using pyElegant\n'
			'!-----------------------------------------------------\n\n'
			).format(filename=self.filename,date=time_string)
		write_string.append(header)
		
		single_line_command_names = ['optimization_term','optimization_variable','optimization_covariable',\
			'optimize','save_lattice']
		single_line_command_names_extra_endline = []
		
		for command in commands:
			#logging.debug(command.name)
			#logging.debug(command.args)
		#for key,item in commands.items():
			if command.name in single_line_command_names:
				write_string.append('&{} '.format(command.name))
				for name, value in command.args.items():
					write_string.append(name + ' = ' + '{},'.format(value))
				write_string.append('&end\n')
			else:
				write_string.append('&{}\n'.format(command.name))
				for name, value in command.args.items():
					write_string.append('\t' + name.ljust(30) + ' = ' + '{},\n'.format(value))
				write_string.append('&end\n\n')	
		
		with open(self.filename,'w') as f:
			f.write(''.join(write_string))
		
class Optimization:
	"""Set up and provide write instructions for elegant optimization"""
	def __init__(self):
		self.setup_params = dict(mode='"minimize"',method='"simplex"',tolerance=1e-10,n_passes=10,n_evaluations=1000,\
			n_restarts=3,verbose=0,output_sparsing_factor=10)
		self.terms = []
		self.optimization_variables = []
		self.optimization_covariables = []
	
	def add_term(self,element_name,beam_attr,value=0.0,arg_string=None):
		""" add a opt term setting a beam attribute to a val if arg_string isn't given
			Example: set betax at 2nd IP = 0.0
			add_term('IP#2','betax',0.0)
		"""
		
		if arg_string:
			self.terms.append(arg_string)
		else:
			string=[]
			string.append('"0')
			if '#' in element_name:
				string.append(element_name)
			else:
				string.append(element_name+'#1')
			
			string[-1] = string[-1] + '.' + beam_attr
			string.append(str(value))
			string.append('-')
			string.append('sqr"')
			self.terms.append({'term':' '.join(string)})
	
	def add_variable(self,element_name,item,lower_limit=0.0,upper_limit=0.0,step_size=0.05):
		self.optimization_variables.append({'name':element_name,'item':item,'lower_limit':lower_limit,'upper_limit':upper_limit,'step_size':step_size})
		
	def add_covariable(self,element_name,item,equation):
		self.optimization_covariables.append({'name':name,'item':item,'equation':equation})
		
	def apply_optimization(self,commands):
		""" Add optimization commands to elegant_commands for writing
			Optimization setup must come before bunched beam -> terms/vars/covars/ -> bunched beam -> optimize -> save lattcie	
		"""
		new_list = []
		
		while len(commands):
			command = commands.pop(0)
			if command.name == 'bunched_beam' or command.name == 'sdds_beam':
				#save old list to append to end after optimization
				old_list = copy.deepcopy(new_list)
			
				new_list.append(Command('optimization_setup',self.setup_params))
				for ele in self.terms:
					new_list.append(Command('optimization_term',ele))
					
				for ele in self.optimization_variables:
					new_list.append(Command('optimization_variable',ele))
					
				for ele in self.optimization_covariables:
					new_list.append(Command('optimization_covariable',ele))
					
				new_list.append(command)
				new_list.append(Command('optimize',{'summarize_setup':1}))
				
				new_lattice_filename = 'opt.lte'
				new_list.append(Command('save_lattice',{'filename':new_lattice_filename}))
				
				old_list[0].args['lattice'] = new_lattice_filename
				logging.debug(old_list[0].args)
				for ele in old_list:
					new_list.append(ele)
				#finally add beam
				new_list.append(command)
				
			else:
				new_list.append(command)
		
		#new_list_command_order = []
		#new_list_commands = {}
		#for ele in new_list:
		#	new_list_command_order.append(list(ele.keys())[0])
		#	new_list_commands[list(ele.keys())[0]] = ele[list(ele.keys())[0]]
		#logging.debug(new_list)
		
		return new_list
					
class Command:
	def __init__(self,name,args={}):
		self.name = name
		self.args = args
		