import sys
import os.path
sys.path.append('Z:\\pyElegant')
import numpy as np
import matplotlib.pyplot as plt
import os.path

import importlib
import importlib.util

from pyElegant import utils

from pyElegant.simulation import lattice_file
from pyElegant.simulation import accelerator
from pyElegant.simulation import special_elements

#run test of a basic python_element

def main():
	file = lattice_file.LatticeFile('test_lattice.lte','w')

	current_dir = os.path.dirname(os.path.abspath(__file__))
	#python_script.main('test.out',current_dir + '\\test')


	#create a beamline
	beamline =  accelerator.Beamline('TEST')

	#add the python_element element using "test.py" as the test script
	#but first need to add the current directory to path
	beamline.beamline_elements.append(special_elements.PythonElement('PYTHON_ELEMENT', os.path.join(current_dir,'test.py'),True))

	#write lattice file
	file.write(beamline)

	utils.run_elegant('test.ele')

if __name__=='__main__':
	main()
