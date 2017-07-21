#tools for phase space calculations

import numpy as np
import logging

def beta(sig,emit):
	return sig**2 / emit
	
def alpha(sigp,emit):
	return sigp**2 /emit

def calcuate_phase_space(data):
	""" take 6D data and calcuate importatn dirstibution moments data = ['x','xp','y','yp','t','p','particleID']"""
	results = {}
	
	results['sx'] = np.std(data['x'])
	results['sxp'] = np.std(data['xp'])
	results['sy'] = np.std(data['y'])
	results['syp'] = np.std(data['yp'])
	results['st'] = np.std(data['t'])
	results['sp'] = np.std(data['p'])
	
	results['avgp'] = np.mean(data['p'])
	
	results['ex'] = emittance([data['x'],data['xp']])
	results['ey'] = emittance([data['y'],data['yp']])
	
	results['betax'] = beta(results['sx'],results['ex'])
	results['betay'] = beta(results['sy'],results['ey'])

	results['alphax'] = alpha(results['sxp'],results['ex'])
	results['alphay'] = alpha(results['syp'],results['ey'])
	
	logging.info('\n' + '\n'.join(['{}:{}'.format(name,val) for name,val in results.items()]))
	
	
	return results

	
def emittance(data):
	""" calcuate the emittance of a set of coordinates data = [x,x']"""
	
	x = data[0]
	xp = data[1]
	N = len(x)
	
	#logging.debug(x)
	#logging.debug(N)
	
	exp_x2 = (1/N) * np.sum((x-np.mean(x))**2)
	exp_xp2 = (1/N) * np.sum((xp-np.mean(xp))**2)
	exp_xxp = (1/N) * np.sum((x-np.mean(x))*(xp-np.mean(xp)))
	
	#logging.debug(np.sqrt(exp_x2))
	#logging.debug(exp_xp2)
	#logging.debug(exp_xxp)
	
	#logging.debug(exp_x2 * exp_xp2)
	#logging.debug(exp_xxp**2)
	
	return np.sqrt(exp_x2 * exp_xp2 - exp_xxp**2)