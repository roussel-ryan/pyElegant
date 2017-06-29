import logging
import numpy as np
from . import library


class Mask:
	def __init__(self,filename):
		self.filename = filename
		self.load_mask_data()
		self.get_mask_method()
		logging.debug(self.mask_method)
		
	def load_mask_data(self):
		self.params = {}
		f = open(self.filename)
		#find mask name
		for line in f:
			if '!' in line:
				pass
			else:
				self.mask_name = line.strip().split(' ')[1]
				break
		#get mask params
		for line in f:
			if '!' in line:
				pass
			else:
				try:
					self.params[line.strip().split(' ')[0]] = float(line.strip().split(' ')[1])
				except ValueError:
					self.params[line.strip().split(' ')[0]] = line.strip().split(' ')[1]
		f.close()
		
	def get_mask_method(self):
		aval_method = {}
		for ele in dir(library):
			if 'mask' in ele:
				aval_method[ele] = getattr(library,ele)
	
		try:
			self.mask_method = aval_method[self.mask_name]
		except KeyError:
			logging.warning('Mask type {} not found!'.format(self.params[mask_name]))
		
	def apply_mask(self,data):
		result = []
		x = data.T[0]
		y = data.T[2]
		for particle,passes_thru in zip(data,[abs(eleY) <= self.mask_method(eleX,**self.params) for eleX,eleY in zip(x,y)]):
			if passes_thru:
				result.append(particle)
		return np.asarray(result)