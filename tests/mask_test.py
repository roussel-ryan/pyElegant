# -*- coding: utf-8 -*-
import logging
import sys

import matplotlib.pyplot as plt
import numpy as np

import context
from pyElegant.beamline import lattice_file
from pyElegant.beamline import masking_script

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	args = sys.argv
	masking_script.main(args[1],'circle_mask.config')
	