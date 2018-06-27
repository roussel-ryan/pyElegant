import numpy as np
import matplotlib.pyplot as plt


def density(xdata,ydata,nLevels=100,xInc=0.1,yInc=0.1,nBins=100):
	xdiff = xdata.max() - xdata.min()
	ydiff = ydata.max() - ydata.min()
	hist2DLimits = [[xdata.min() - xInc*xdiff,xdata.max() + xInc*xdiff],[ydata.min() - yInc*ydiff,ydata.max() + yInc*ydiff]]
	H, xedges, yedges = np.histogram2d(xdata,ydata,range=hist2DLimits,bins=nBins)
	H = H.T
	#get centers
	xcenters = (xedges[:-1] + xedges[1:]) / 2
	ycenters = (yedges[:-1] + yedges[1:]) / 2

	X,Y = np.meshgrid(xcenters,ycenters)
	l = np.linspace(H.min(),H.max(),nLevels)
	
	return X,Y,H,l