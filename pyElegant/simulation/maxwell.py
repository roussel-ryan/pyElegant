import numpy as np
import sdds
import logging
import os

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def maxwell_data_to_sdds(data,sdds_file_name='maxwell_fld.sdds'):
    output_file = sdds.SDDS(1)
    t_data = data.T
    names = ('x','y','z','Bx','By','Bz')
    units = ('m','m','m','T','T','T')

    paged_result = [[col.tolist()] for col in t_data]

    for name,unit,item in zip(names,units,paged_result):
        output_file.columnName.append(name)
        output_file.columnDefinition.append([name,unit,'','',output_file.SDDS_DOUBLE,int(len(item[0]))])
        output_file.columnData.append(item)

    output_file.save(sdds_file_name)
    os.system('sddssort {} -column=z,incr -column=y,incr -column=x,incr'.format(sdds_file_name))

def shift_field(data,vector=[0.0,0.0,0.0]):
    new_data = np.array([[0,0,0,0,0,0]])
    v = np.append(vector,[0.0,0.0,0.0],axis=0)
    for ele in data:
        new_data = np.append(new_data,[ele + v],axis=0)
    return new_data

def mirror_field(data,mirror_plane='xy',parity='even'):
    '''
        mirror fields and add to quiver coordinates

        - data = field data in shape 6 x N where N = Nx*Ny*Nz is the number of points
        - mirror_plane = plane over which to do mirroring options are {xy,xz,yz}
    '''
    new_data = np.array([[0,0,0,0,0,0]])
    pos_multiplier = {'xy':np.array([1.0,1.0,-1.0]),'yz':np.array([-1.0,1.0,1.0]),'xz':np.array([1.0,-1.0,1.0])}
    parity_multiplier = {'even':np.array([1.0,1.0,1.0]),'odd':np.array([-1.0,-1.0,-1.0])}

    multiplier = np.array([pos_multiplier[mirror_plane],pos_multiplier[mirror_plane]*parity_multiplier[parity]]).flatten()

    #logging.debug(multiplier)
    for ele in data:
        new_data = np.append(new_data,[ele],axis=0)

        m_ele = ele*multiplier
        if m_ele[0] == ele[0] and m_ele[1] == ele[1] and m_ele[2] == ele[2]:
            pass
        else:
            new_data = np.append(new_data,[m_ele],axis=0)

    return new_data[1:]

def plot_3d_field(data):
    t_data = data.T
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.quiver(t_data[0],t_data[1],t_data[2],t_data[3],t_data[4],t_data[5],length=0.01,normalize=True)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    plt.show()

def import_maxwell_data(maxwell_file_name):

    f = open(maxwell_file_name)

    f.readline()
    f.readline()

    data = []
    for line in f:
        if not 'Nan' in line or line.strip()=='':
            data.append(line.rstrip().replace('  ',' ').split(' '))
    return np.asfarray(data)

def write_maxwell_grid(mins,maxs,n_pts = (10,10,10),filename='maxwell_grid.pts'):
    if len(mins) == 3 and len(maxs) == 3 and len(n_pts) == 3:
        with open(filename,'w') as f:
            x = np.linspace(mins[0],maxs[0],n_pts[0])
            y = np.linspace(mins[1],maxs[1],n_pts[1])
            z = np.linspace(mins[2],maxs[2],n_pts[2])
            for i in x:
                for j in y:
                    for k in z:
                        f.write('{} {} {}\n'.format(i,j,k))
    else:
        raise IndexError('mins,maxs and n_pts must be length 3 for maxwell')
