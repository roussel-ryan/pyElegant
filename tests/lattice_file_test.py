# -*- coding: utf-8 -*-
import logging

import context
from pyElegant.beamline_creator import lattice_file

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	f = lattice_file.LatticeFile('testLattice.lte')
	elements = f.read()
	logging.debug(elements['EEX'].get_element('TCAV').parameters)
	logging.debug(elements['DEEX'].is_zipped)
	w = lattice_file.LatticeFile('testWrite.lte','w')
	logging.debug(elements['EEX'].print_element_names())
	DEEX = elements['DEEX']
	EEX = elements['EEX']
	w.write([EEX,DEEX])