# -*- coding: utf-8 -*-
import sys
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import sdds

from autoScaleTicks import *
from . import accelerator
from .masks import mask

class MaskElement(accelerator.BeamlineElement):
	def __init__(self,name,mask_file,keep_files = False):
		self.name = name
		self.mask_file = mask_file

		dir_path = os.path.dirname(os.path.abspath(__file__))
		script_filename = dir_path + '\\masking_script.py'

		if keep_files:
			kf = 1
		else:
			kf = 0

		params = {'COMMAND':'\"python {} %i {}\"'.format(script_filename,self.mask_file),'rootname':'\"mask\"',\
		'input_extension':'\"in\"',\
		'output_extension':'\"out\"',\
		'KEEP_FILES':str(kf),\
		'DRIFT_MATRIX':'1',\
		'USE_CSH':'0'}

		accelerator.BeamlineElement.__init__(self,self.name,'SCRIPT',params)

	def plot_mask(self,axes=None):
		"""
			plot the mask outline, on top of data if axes is given
		"""

		mask_obj = mask.Mask(self.mask_file)
		#logging.debug(mask_obj.params)
		x_scale = mask_obj.params['sigx']
		x_mult = 5

		x = np.linspace(-x_mult*x_scale,x_mult*x_scale)
		y = np.asfarray([mask_obj.mask_method(pt,**mask_obj.params) for pt in x])
		if axes:
			x_mult = axes.x_autoscale_params[1]
			y_mult = axes.y_autoscale_params[1]

			x = x/x_mult
			y = y/y_mult

			axes.plot(x,y,'orange')
			axes.plot(x,-y,'orange')
			axes.set_xlim((np.min(x),np.max(x)))
		else:
			fig,ax = plt.subplots()
			ax.plot(x,y,'orange')
			ax.plot(x,-y,'orange')

class MultipoleElement(accelerator.BeamlineElement):
	def __init__(self,name,element_length,multipole_strength,skew_strength=None,**kwargs):
		self.name = name
		self.orders = list(range(1,len(multipole_strength)))
		self.filename = 'multipole.sdds'

		if skew_strength:
			self.skew_strength = skew_strength
		else:
			self.skew_strength = [0.0] * len(multipole_strength)

		self.data = [self.orders,self.multipole_strength,self.skew_strength]
		output_file = sdds.SDDS(1)

		names = ('order','KnL','JnL')
		units = ('None','1/m^n','1/m^n')
		paged_result = [[col] for col in self.data]
		for name,unit,item in zip(names,units,paged_result):
	        output_file.columnName.append(name)
	        output_file.columnDefinition.append([name,unit,'','',output_file.SDDS_DOUBLE,int(len(item[0]))])
	        output_file.columnData.append(item)

		params = {'L':element_length,'FILENAME':self.filename}
		for name,item in kwargs.items():
			params[name] = item

		output_file.save(self.filename)
		accelerator.BeamlineElement.__init__(self,self.name,'FMULT',params)


if __name__=='__main__':
	test_element = MaskElement('test',None)
	print(test_element.parameters)
