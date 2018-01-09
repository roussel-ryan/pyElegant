# -*- coding: utf-8 -*-
import sys
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import sdds

from . import accelerator

class PythonElement(accelerator.BeamlineElement):
	'''
		PythonElement(name,python_file,keep_files = False)
			Handles making a elegant beamline element that uses a python script to
			create an arbitrary shaped mask for killing off particles
			
			name = beamline element name used as refereance in the elegant .lte file
			python_file = python file with a function "main" defined that has the following reuirements
				- must be in the form main(data) where data is a 7xN numpy array that
					represents the particle distribution of N particles going into the beamline element
					where each array element should be in the form (x,xp,y,yp,t,p,ParticleID)
				- main must return a 7xM array that represents the particle distribution after
					the beamline element with M particles (Note: M != N or M = N)
					where each array element should be in the form (x,xp,y,yp,t,p,ParticleID)
			
	'''


	def __init__(self,name,python_file,keep_files = False):
		self.name = name
		self.python_file = python_file

		dir_path = os.path.dirname(os.path.abspath(__file__))
		script_filename = dir_path + '\\scripts\\python_script.py'

		params = {'COMMAND':'\"python {} %i {}\"'.format(script_filename,self.python_file),'rootname':'\"mask\"',\
		'input_extension':'\"in\"',\
		'output_extension':'\"out\"',\
		'KEEP_FILES':str(int(keep_files)),\
		'DRIFT_MATRIX':'1',\
		'USE_CSH':'0'}

		accelerator.BeamlineElement.__init__(self,self.name,'SCRIPT',params)

	# def plot_mask(self,axes=None):
		# """
			# plot the mask outline, on top of data if axes is given
		# """

		# mask_obj = mask.Mask(self.mask_file)
		# #logging.debug(mask_obj.params)
		# x_scale = mask_obj.params['sigx']
		# x_mult = 5

		# x = np.linspace(-x_mult*x_scale,x_mult*x_scale)
		# y = np.asfarray([mask_obj.mask_method(pt,**mask_obj.params) for pt in x])
		# if axes:
			# x_mult = axes.x_autoscale_params[1]
			# y_mult = axes.y_autoscale_params[1]

			# x = x/x_mult
			# y = y/y_mult

			# axes.plot(x,y,'orange')
			# axes.plot(x,-y,'orange')
			# axes.set_xlim((np.min(x),np.max(x)))
		# else:
			# fig,ax = plt.subplots()
			# ax.plot(x,y,'orange')
			# ax.plot(x,-y,'orange')

class MultipoleElement(accelerator.BeamlineElement):
	def __init__(self,name,element_length,multipole_strength,skew_strength=None,**kwargs):
		self.name = name
		self.orders = list(range(1,len(multipole_strength)+1))
		self.filename = '{}_multipole.sdds'.format(self.name)
		self.multipole_strength = multipole_strength

		if skew_strength:
			self.skew_strength = skew_strength
		else:
			self.skew_strength = [0.0] * len(multipole_strength)

		self.data = [self.orders,self.multipole_strength,self.skew_strength]
		output_file = sdds.SDDS(1)

		names = ('order','KnL','JnL')
		units = ('None','1/m^n','1/m^n')
		data_types = (output_file.SDDS_INT16,output_file.SDDS_DOUBLE,output_file.SDDS_DOUBLE)
		for ele in self.data:
			logging.debug(len(ele))

		paged_result = [[col] for col in self.data]
		for name,unit,item,data_type in zip(names,units,paged_result,data_types):
			output_file.columnName.append(name)
			output_file.columnDefinition.append([name,unit,'','',data_type,0])
			output_file.columnData.append(item)

		params = {'L':element_length,'FILENAME':self.filename}
		for name,item in kwargs.items():
			params[name.upper()] = item

		output_file.save(self.filename)
		accelerator.BeamlineElement.__init__(self,self.name,'FMULT',params)

class KQuadElement(accelerator.BeamlineElement):
	def __init__(self,name,element_length,ref_radius,multipole_strength,**kwargs):
		self.name = name

		self.filename = '{}_kquad.sdds'.format(self.name)

		self.ref_radius = ref_radius
		self.quad_strength = multipole_strength[0]
		self.multipole_strength = multipole_strength[1:]
		self.orders = list(range(2,len(self.multipole_strength)+2))

		self.f_strength = []
		for order,m_strength in zip(self.orders,self.multipole_strength):
			self.f_strength.append(m_strength * self.ref_radius ** order /self.quad_strength)

		#if skew_strength:
			#self.skew_strength = skew_strength
		#else:
		self.skew_strength = [0.0] * len(self.multipole_strength)

		self.data = [self.orders,self.f_strength,self.skew_strength]
		output_file = sdds.SDDS(1)

		names = ('order','normal','skew')
		units = ('None','None','None')
		data_types = (output_file.SDDS_INT16,output_file.SDDS_DOUBLE,output_file.SDDS_DOUBLE)
		for ele in self.data:
			logging.debug(len(ele))

		output_file.defineParameter('referenceRadius','','m','','',output_file.SDDS_DOUBLE,'')
		output_file.setParameterValue('referenceRadius',self.ref_radius,1)

		paged_result = [[col] for col in self.data]
		for name,unit,item,data_type in zip(names,units,paged_result,data_types):
			output_file.columnName.append(name)
			output_file.columnDefinition.append([name,unit,'','',data_type,0])
			output_file.columnData.append(item)

		params = {'L':element_length,'K1':self.quad_strength,'SYSTEMATIC_MULTIPOLES':self.filename}
		for name,item in kwargs.items():
			params[name.upper()] = item

		output_file.save(self.filename)
		accelerator.BeamlineElement.__init__(self,self.name,'KQUAD',params)

if __name__=='__main__':
	test_element = MaskElement('test',None)
	print(test_element.parameters)
