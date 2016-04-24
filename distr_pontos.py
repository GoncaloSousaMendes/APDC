# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:51:09 2016
distribui pontos
@author: Moncada
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import quateriongen as qt
from sklearn.preprocessing import normalize

def randoms(n = 500):
    
    rands = np.random.uniform(-10,10,(n,3))
    rands = normalize(rands, axis=1, norm='l1')
    return rands
    
    
def dist(base_set, point):
    x = point
    y = base_set
    #print x
    #print y
    res = np.zeros((base_set.shape[0]))
    for ix in range (len(y)):
        res[ix] = np.sqrt(np.sum((x-y[ix])**2))
    
    #res = np.sqrt(np.sum((x-y)**2))
    #print res
    
    #devolver o mais perto
    return res[min]
    
def evaluate(points):
    """
    return array with min distances
    and a structure with the number of quaternion
    closer to him, with quaternios matrices, which matrice with 
    two lines, the first whith the number of the closer quaternion
    (acording to its position on the rot_points)
    and the second line containing that distance
    """
    res = np.ndarray(points.shape[0])
    # estrutura que guarda o quaterniao mais proximo
    # e a distancia entre eles
    bindings = np.zeros((points.shape[0], 2, 1))
    #print "begin evaluate"
    #print res
    for ix in range(len(res)):
        if ix==0:
            base_sets = points[1:]
        elif ix==len(res)-1:
            base_sets = points[:-1]
        else:
            base_sets = np.concatenate((points[:ix],points[ix+1:]))  
            
            #numpy.sqrt(numpy.sum((x-y)**2))  
            
        #diffs = base_sets[:]-points[ix]
        #dists = np.sum(np.square(diffs),axis=-1)
        dists = point_dists(base_sets[:], points[ix])
        
        #print "point ", ix, ": ", points[ix] 
        #print dists 
        #maxd = np.max(dists,axis=-1)  
        #print maxd
        # nota: maxd contèm as distancias do quaternião presente
        # a todos os outros    
        #res[ix] = np.min(dists)
        #print maxd
        
        min = 9999
        #refere-se a posicao no rot_points
        point_number = 0
        for iz in range (0,len(dists)):
            if dists[iz] <= min:
                min = dists[iz]
                if (iz < ix):
                    point_number = iz
                else:
                    point_number = iz+1

        bindings[ix,0,0] = point_number
        bindings[ix,1,0] = min
        res[ix] = min
        #print "iteração: ", ix
        #print dists
        #print res[ix]
        
    return res, bindings

    
def point_dists(base_sets,new_sets):
    """
    return vector of max distances between each
    new_points to base_ponts
    """
    res = np.zeros(new_sets.shape[0])
    for ix in range(len(res)):
        diffs = base_sets[:]-new_sets[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        #print "dists: ",dists
        #maxd = np.max(dists,axis=-1)     
        #print "maxd: ",maxd
        res[ix] = np.min(dists)
        #print res[ix]
        #print "\n"
    #print res
    return res

def spread_points(num=100,points_per_step=100):
    """
    return a spread of num quaternions
    """
    #cria uma matrix de zeros num por 4
    points = np.zeros((num,3))
    #print quats
    #a primeira posição de quats fica =
    points[0,:] = [0, 0, 0]
    #normed_matrix = normalize(matrix, axis=1, norm='l1')
    points = normalize(points, axis=1, norm='l1')
    #print points[0,:]
    #print quats
    #print rot_points
    for ix in range(1,num):
        # criar quats_per_step quaterniões aleatorios 
        rand_points = randoms(points_per_step) 

        # ver as distancias (retorna já os mais proximos!)
        dists = point_dists(points[:ix],rand_points)
        # ir buscar o maximo das distancias mais proximas
        new_rot = np.argmax(dists)
        #print dists
        points[ix,:]=rand_points[new_rot,:]
        #points[ix,:] = dists

    #print "number of quaternions: ",len(quats)    
    return points
    
    
if __name__ == '__main__':                
    
    ptsOnSphere = np.zeros((10,3)) 
    #ptsOnSphere = GetPointsEquiAngularlyDistancedOnSphere(500)
    #ptsOnSphere = ptsOnSphere / ptsOnSphere.max(axis=0)
    ptsOnSphere =  spread_points(100,100)
    mins, bind = evaluate(ptsOnSphere)
    #print bind
    mediana, av, variancia = qt.draw_kde(mins, 'distribution_'+str(ptsOnSphere.shape[0])+'_new_dist.png', np.max(ptsOnSphere)/ptsOnSphere.shape[0])
    print mediana
    print av
    print variancia
    if(True):
        from numpy import *
        import pylab as p
        import mpl_toolkits.mplot3d.axes3d as p3

        fig=p.figure()
        ax = p3.Axes3D(fig)

        x_s=[];y_s=[]; z_s=[]

        for pt in ptsOnSphere:
            x_s.append( pt[0]); y_s.append( pt[1]); z_s.append( pt[2])

        ax.scatter3D( array( x_s), array( y_s), array( z_s) )                
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
        p.show()
        #end    