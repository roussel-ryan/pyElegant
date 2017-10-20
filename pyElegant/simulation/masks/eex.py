import numpy as np
from scipy import special
from PrintVars import PrintVars

#methods = {'maskCircle':maskCircle,'maskLinear':'maskLinear',\
#	'maskUniform':maskUniform,\
#	'maskWWitness':maskWWitness}

def maskCircle(x,r=10):
	if x < -r:
		return 0
	elif x >= -r and x < r:
		return np.sqrt(r**2 - x**2)
	else:
		return 0

def maskWWitness(x,sigx=0,sigy=0,g0=100,g1=3e4,w0=4e-3,d=1e-3,w1=1e-4,h=100):

	if x < -g0/g1:
		g = 0
	elif x >= -g0/g1 and x < -g0/g1 + w0:
		g = g0 + g1*x
	elif x >= -g0/g1 + w0 and x < -g0/g1 + w0 + d - w1/2.:
		g = 0
	elif x >= -g0/g1 + w0 + d - w1/2. and x < -g0/g1 + w0 + d + w1/2.:
		g = h
	else:
		g = 0

	nu = np.sqrt(2)*sigy*special.erfinv(-sigx*g*np.exp(x**2 / (2.0*sigx**2)))
	if abs(nu) == np.inf:
		return 0.0
	else:
		return nu

def maskLinear(x,sigx=0,sigy=0,g0=100,g1=5e4):
	nu = -np.sqrt(2)*sigy*special.erfinv(-sigx*(g0+g1*x)*np.exp(x**2 / (2.0*sigx**2)))
	#PrintVars(locals())
	if abs(nu) == np.inf:
		return 0.0
	elif nu < 0.0:
		return 0.0
	else:
		return nu


def maskUniform(x,sigx=0,sigy=0,h=100):
	nu = -np.sqrt(2)*sigy*special.erfinv(-sigx*(h)*np.exp(x**2 / (2.0*sigx**2)))
	if abs(nu) == np.inf:
		return 0.0
	elif nu < 0.0:
		return 0.0
	else:
		return nu
