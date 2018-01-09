import numpy as np
import matplotlib.pyplot as plt

from .. import utils
from autoScaleTicks import *

def plot_SDDS(x,y,filename,*args,axes=None,**kwargs):

	if axes:
		ax = axes
	else:
		fig,ax = plt.subplots()

	data_params,data_cols = utils.read_sdds_file(filename)

	try:
		ax.plot(data_cols[x],data_cols[y],*args,**kwargs)
	except KeyError:
		logging.warning('Key not found in {}'.format(filename))

	return ax

def plot_phase_space(filename, density=False, title=None, reduced=False):
	"""
		plotPhaseSpace(filename,density=False)
			- filename = SDDS file output which has screen-like data points from elegant
			- density = Flag to specify scatter plot vs density plot (which will take longer)
	"""
	c = 2.998e8
	data_params,data_cols = utils.read_sdds_file(filename)
	col_names = ['x','xp','y','yp','t','p','particleID']
	data = []
	for name in col_names:
		data.append(data_cols[name])

	screenData = np.asfarray(data)
	#PrintVars(locals())
	#logging.debug(screenData)
	if reduced:
		fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(7,7))
	else:
		fig,((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(12,7))

	if density:
		if reduced:
			density_plot(screenData[0],screenData[2],ax1,labels=['x','y'],units=['m','m'])
			density_plot(screenData[0],screenData[1],ax2,labels=['y','yp'],units=['m',''])
			density_plot(screenData[2],screenData[3],ax3,labels=['x','xp'],units=['m',''])
			density_plot(screenData[4]-np.mean(screenData[4]),screenData[5],ax4,labels=['t','r$\gamma\beta$'],units=['s',''])
		else:
			density_plot(screenData[0],screenData[2],ax1,labels=['x','y'],units=['m','m'])
			density_plot(screenData[4]-np.mean(screenData[4]),screenData[0],ax2,labels=['t','x'],units=['s','m'])
			density_plot(screenData[4]-np.mean(screenData[4]),screenData[2],ax3,labels=['t','y'],units=['s','m'])
			density_plot(screenData[0],screenData[1],ax4,labels=['x','xp'],units=['m',''])
			density_plot(screenData[2],screenData[3],ax5,labels=['y','yp'],units=['m',''])
			density_plot(screenData[4]-np.mean(screenData[4]),screenData[5],ax6,labels=['t','r$\gamma\beta$'],units=['s',''])
	else:
		if reduced:
			ax1.plot(screenData[0],screenData[2],'.',ms=1)
			autoScale2D(ax1,ylabel='y',xlabel='x',yUnits='m',xUnits='m')

			ax3.plot(screenData[0],screenData[1],'.',ms=1)
			autoScale2D(ax3,ylabel='xp',xlabel='x',yUnits='',xUnits='m')

			ax2.plot(screenData[2],screenData[3],'.',ms=1)
			autoScale2D(ax2,ylabel='yp',xlabel='y',yUnits='',xUnits='m')

			ax4.plot((screenData[4]-np.mean(screenData[4])),screenData[5],'.',ms=1)
			autoScale2D(ax4,ylabel=r'$\gamma\beta$',xlabel='t',yUnits='',xUnits='s')
		
		else:
			ax1.plot(screenData[0],screenData[2],'.')
			autoScale2D(ax1,ylabel='y',xlabel='x',yUnits='m',xUnits='m')

			ax2.plot((screenData[4]-np.mean(screenData[4])),screenData[0],'.')
			autoScale2D(ax2,ylabel='x',xlabel='t',yUnits='m',xUnits='s')

			ax3.plot((screenData[4]-np.mean(screenData[4])),screenData[2],'.')
			autoScale2D(ax3,ylabel='y',xlabel='t',yUnits='m',xUnits='s')

			ax4.plot(screenData[0],screenData[1],'.')
			autoScale2D(ax4,ylabel='xp',xlabel='x',yUnits='',xUnits='m')

			ax5.plot(screenData[2],screenData[3],'.')
			autoScale2D(ax5,ylabel='yp',xlabel='y',yUnits='',xUnits='m')

			ax6.plot((screenData[4]-np.mean(screenData[4])),screenData[5],'.')
			autoScale2D(ax6,ylabel=r'$\gamma\beta$',xlabel='t',yUnits='',xUnits='s')
	if title:
		ax2.set_title(title)
	else:
		ax2.set_title('Phase space plot from file ' +filename)
	fig.tight_layout()


	return fig

def density_plot(xdata,ydata,ax,labels=['',''],units=['',''],nLevels=100,xInc=0.1,yInc=0.1,colorbar=False):
	xdiff = xdata.max() - xdata.min()
	ydiff = ydata.max() - ydata.min()
	hist2DLimits = [[xdata.min() - xInc*xdiff,xdata.max() + xInc*xdiff],[ydata.min() - yInc*ydiff,ydata.max() + yInc*ydiff]]
	H, xedges, yedges = np.histogram2d(xdata,ydata,range=hist2DLimits,bins=100)
	H = H.T
	#get centers
	xcenters = (xedges[:-1] + xedges[1:]) / 2
	ycenters = (yedges[:-1] + yedges[1:]) / 2

	X,Y = np.meshgrid(xcenters,ycenters)
	l = np.linspace(H.min(),H.max(),nLevels)
	autoScale3D(ax,X,Y,H,xlabel=labels[0],ylabel=labels[1],xUnits=units[0],yUnits=units[1],levels=l)

	return ax

def get_2D_data(axes):
	axesData=[]
	axesLines = axes.get_lines()
	for ele in axesLines:
		axesData.append([ele.get_xdata(),ele.get_ydata()])
	return axesData

def histogram_overlay(axes,data=[],axis='x',inc=0.25,label='',line_number=0):
	"""
		add a histogram overlay to axes object,data supplied by axes itself or data supplied by user
		data supplied by user is prioritized over data supplied by graph
	"""
	axis_dict = {'x':0,'y':1}

	if len(data):
		hist_data = data[axis_dict[axis]]
		xLimits = (hist_data.min(),hist_data.max())
	else:
		graph_data = get_2D_data(axes)[line_number]
		if len(graph_data):
			hist_data = graph_data[axis_dict[axis]]
			xLimits = axes.get_xlim()
		else:
			raise RuntimeError('No data to create histogram overlay')



	xPrefix, xMult, xTextMult = autoScaleAxis(xLimits)
	diff = xLimits[1] - xLimits[0]
	histLimits = [xLimits[0] - inc*diff,xLimits[1] + inc*diff]
	hist, bin_edges = np.histogram(hist_data*xMult,range=histLimits,bins='auto')
	bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
	ax2 = axes.twinx()
	if axis=='x':
		ax2.plot(bin_centers,hist/np.max(hist),'r-',label='x Axis Histogram')
	else:
		ax2.plot(hist/np.max(hist),bin_centers,'r-',label='x Axis Histogram')

	if label:
		ax2.set_ylabel(label + ' (Arb. U.)')
	else:
		ax2.set_ylabel('Hist(' + axes.get_xlabel().split(' ')[0] +') (Arb. U.)')
	ax2.set_xlim(xLimits)
	return ax2
