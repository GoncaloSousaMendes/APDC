# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:11:25 2016

Testar o hillClimbing

@author: Moncada
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from math import cos, sin, pi, sqrt
from sklearn.preprocessing import normalize
import distr_pontos as dp


def randoms(n = 500):
    
    rands = np.random.rand(n,3)
    unif_rand = rands / rands.max(axis=0)
    return unif_rand
    
def GetPointsEquiAngularlyDistancedOnSphere(numberOfPoints=1000):
    """ each point you get will be of form 'x, y, z'; in cartesian coordinates
        eg. the 'l2 distance' from the origion [0., 0., 0.] for each point will be 1.0 
        ------------
        converted from:  http://web.archive.org/web/20120421191837/http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere ) 
    """
    points = np.zeros((numberOfPoints/2, 3))
    
    dlong = pi*(3.0-sqrt(5.0))  # ~2.39996323 
    dz   =  2.0/numberOfPoints
    long =  0.0
    z    =  1.0 - dz/2.0
    #ptsOnSphere =[]
    for k in range( 0, numberOfPoints): 
        r = sqrt(1.0-z*z)
        ptNew = (cos(long)*r, sin(long)*r, z)
        #ptsOnSphere.append( ptNew )
        points[k] = ptNew
        z    = z - dz
        long = long + dlong
        # so queremos em metade da esfera
        if(k == (numberOfPoints/2)-1):
            break
    return points
    

def hill(points, bindings, mediana, variancia, av  ):
    print "\nHill climbing all to median"
    #vamos sempre trabalhar com os quaternioes antigos, e guardar nas estrutras novas!

    new_set_points = np.copy(points)
    
    medStart = np.copy(mediana)
    # Rever o valor
    to_much = 2
    it = 0
    accepted = 0
    var = np.copy(variancia)
    while ( it < number_it):
        for n_q in range (0, bindings.shape[0]):
            dist_mediana = bindings[n_q, 1,0]
            if  (dist_mediana != mediana):
                # arranjar randons
                randoms = np.random.uniform(-1,1,(number_of_randoms,3))
                # temos de mexer pouco nos quaternioes, por isso temos de somar valores baixos
                randoms = np.divide(randoms, value_to_divide)
                # alterar os valores pelo numeros random
                # nesta posição bindings[n_q,0,0] está o numero do quaternião que está mais proximo
                news_points = np.sum((randoms, points[  int(bindings[n_q,0,0])  ]))
                # mexemos nos quaterniões, temos de normalizalos 
                unif_points = news_points / news_points.max(axis=0)

                
                dists = dist(unif_points, points[  int(bindings[n_q,0,0])  ])
                
                if (dist_mediana < mediana):                
                
                    for iz in range (0,len(dists)):
                        if (dists[iz] > dist_mediana) & (dists[iz] < (mediana + to_much)):
                            #guardar o novo ponto
                            new_set_points[ int(bindings[n_q,0,0]) ] = unif_points[iz]
                            if stop_at_first == 1:
                                break;
               
                elif (dist_mediana > mediana):
                     for iz in range (0,len(dists)):
                         if (dists[iz] < dist_mediana) & (dists[iz] > (mediana - to_much)):
                              #guardar o novo ponto
                            new_set_points[ int(bindings[n_q,0,0]) ] = unif_points[iz]
                            if stop_at_first == 1:
                                break;
       
        
        mins, bindings2 = evaluate(new_set_points)
        var_old = np.copy(var)
        varTemp = np.var(mins)
        me = np.median (mins)
        it = it +1
        if ((varTemp-var_old) < 0.):
            points = np.copy(new_set_points)
            var = np.copy(varTemp)
            accepted = accepted + 1
            bindings = np.copy(bindings2)
            mediana = np.copy(me)
        else:
            var = np.copy(var_old)
    
    mins,b = evaluate(points)
    mediana2, av2, var2 = draw_kde(mins,'distribution_new_'+str(points.shape[0])+'_test.png', np.max(mins)/ptsOnSphere.shape[0])
    print "Variancia antiga: ", variancia, " Variancia nova: ", var2, " diferença: ", var2-variancia
    print "Mediana antiga: ", medStart, " Nova mediana: ", mediana2 
    print "Media antiga: ", av, " Nova media: ", av2

    return var2-variancia, accepted, points



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
    
    return res
    
    
    
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
        dists = dist(base_sets[:], points[ix])
        
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
    
def draw_kde(vals,image_file, band = 0.75):

    me = np.median (vals)    
    print me
    av = np.average (vals)    
    print av
    var = np.var(vals)
    print var
    
    #shapiro wilk test
    #s = scipy.stats.shapiro(vals)
    #print "shapiro: ", s
    
    #k = scipy.stats.kurtosis(vals,axis=0, fisher=False, bias=True)
    #print "kurtosis: ", k
    
    kde = KernelDensity(kernel='gaussian', bandwidth=band).fit(vals[:,np.newaxis])
    plt.figure(figsize=(12,8))
    xs = np.linspace(0, max(vals)*1.2, 1000)[:, np.newaxis]
    ys = np.exp(kde.score_samples(xs))
    plt.plot(xs,ys,'-b', linewidth=3)
    plt.savefig(image_file,dpi=300,bbox_inches='tight')
    plt.close()
    return me, av, var

#numpy.sqrt(numpy.sum((x-y)**2))    

if __name__ == '__main__':                
    
    ptsOnSphere = np.zeros((250,3)) 
    ptsOnSphere = GetPointsEquiAngularlyDistancedOnSphere(500)
    ptsOnSphere = ptsOnSphere / ptsOnSphere.max(axis=0)
    #ptsOnSphere = normalize(ptsOnSphere, axis=1, norm='l1')
    #ptsOnSphere =  randoms(100)
    
    ptsOnSphere = dp.spread_points(100,300)
    
    mins, bind = evaluate(ptsOnSphere)
    #print bind
    mediana, av, variancia = draw_kde(mins, 'distribution_'+str(ptsOnSphere.shape[0])+'_new_test.png', np.max(mins)/ptsOnSphere.shape[0])
    
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
  
    value_to_divide = 1
    number_of_randoms = 100
    number_it = 10
    stop_at_first = 0
    
    a, v, pts = hill(ptsOnSphere, bind, mediana, variancia, av  )
    
    print len(ptsOnSphere)
    #toggle True/False to print them
    if( False ):
        for pt in ptsOnSphere:  print(pt)

    #toggle True/False to plot them
    if(True):
        from numpy import *
        import pylab as p
        import mpl_toolkits.mplot3d.axes3d as p3

        fig=p.figure()
        ax = p3.Axes3D(fig)

        x_s=[];y_s=[]; z_s=[]

        for pt in pts:
            x_s.append( pt[0]); y_s.append( pt[1]); z_s.append( pt[2])

        ax.scatter3D( array( x_s), array( y_s), array( z_s) )                
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
        p.show()
        #end

