import sys
import os.path
sys.path.append('Z:\\pyElegant')
import numpy as np
import matplotlib.pyplot as plt

import importlib
import importlib.util

from pyElegant import utils

from pyElegant.simulation import lattice_file
from pyElegant.simulation import accelerator
from pyElegant.simulation import special_elements
from pyElegant.simulation.scripts import python_script

#run test of a basic python_element

def main():
	file = lattice_file.LatticeFile('test_lattice.lte','w')
	
	m = importlib.import_module('test')
	current_dir = os.path.dirname(os.path.abspath(__file__))
	python_script.main('test.out',current_dir + '\\test')
	
	
	#create a beamline
	beamline =  accelerator.Beamline('TEST')
	
	#add the python_element element using "test.py" as the test script 
	#but first need to add the current directory to path
	current_dir = os.path.dirname(os.path.abspath(__file__))
	sys.path.insert(0,current_dir)
	beamline.beamline_elements.append(special_elements.PythonElement('PYTHON_ELEMENT','.'))
	
	#write lattice file
	file.write(beamline)
	
	utils.run_elegant('test.ele')
	
if __name__=='__main__':
	main()