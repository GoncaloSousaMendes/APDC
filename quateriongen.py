# -*- coding: utf-8 -*-
"""
script para distribuir quaterniões
tem tambem as funções necessarias para lidar com quaterniões:
- random_quaternions
- multiply_quaternions
- conjugate
- rotate_points
- point_dists
- point_dists_mine
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

import math


def random_quaternions(count=100):
    """
    return a matrix with count random quaternions
    each quaternion is a line
    """
    #matrix de count por 3, cheios de numeros aleatorios
    rands = np.random.rand(count,3)
    # todos as posições zero de cada linha
    root_1 = np.sqrt(rands[:,0])
    # equivalente a math.sqrt(1-u1), usando a primeira posição de cada linha
    minus_root_1 = np.sqrt(1-rands[:,0])
    two_pi_2 = np.pi*2*rands[:,1]
    two_pi_3 = np.pi*2*rands[:,2]
    
    res = np.zeros((count,4))
    res[:,0] = minus_root_1*np.sin(two_pi_2)
    res[:,1] = minus_root_1*np.cos(two_pi_2)
    res[:,2] = root_1*np.sin(two_pi_3)
    res[:,3] = root_1*np.cos(two_pi_3)
    
    return res
    
def multiply_quaternions(quats1,quats2):
    """
    return matrix (len,4) for pairwise multiplication of
    quaternions. Matrices quats1 and quats2 must have
    same number of lines and 4 columns
    """
    w1 = quats1[:,0]
    x1 = quats1[:,1]
    y1 = quats1[:,2]
    z1 = quats1[:,3]

    w2 = quats2[:,0]
    x2 = quats2[:,1]
    y2 = quats2[:,2]
    z2 = quats2[:,3]

    res = np.zeros((quats1.shape[0],4))
    
    res[:,0] = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    res[:,1] = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    res[:,2] = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    #res[:,3] = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    res[:,3] = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return res
    
def conjugate(quats):
    """
    return conjugates of quaternions
    """
    res = np.zeros(quats.shape)
    res[:,0]=quats[:,0]
    res[:,1]=-quats[:,1]
    res[:,2]=-quats[:,2]
    res[:,3]=-quats[:,3]
    
    return res
  
def rotate_points(points,quaternions):
    """
    return matrix with rotated points
    points is matrix of points lines and 3 columns
    quaternions is a matrix with quaternion lines and 4 columns
    result is a matrix with (quaternions, points, 3) dimensions
    """
    
    res = np.zeros((quaternions.shape[0],points.shape[0],4))  
    #print res    
    # cada matrix sera igual ao points, a excepção das primeiras filas
    res[:,:,1:] = points   
    #print res    
    # vai buscar os conjugates...
    conjugates = conjugate(quaternions)    
    #print conjugates
    
    # ficamos com o ponto 'rodado' 
    for ix in range(len(points)):
        res[:,ix,:] = multiply_quaternions(quaternions,res[:,ix,:])
        res[:,ix,:] = multiply_quaternions(res[:,ix,:],conjugates)
    return res[:,:,1:]

def point_dists(base_sets,new_sets):
    """
    return vector of max distances between each
    new_points to base_ponts
    """
    res = np.zeros(new_sets.shape[0])
    for ix in range(len(res)):
        #diferenças entre todos os pontos
        diffs = base_sets[:]-new_sets[ix]
        # assume a forma (diff(x)^2 + diff(y)^2 + diff(z)^2)
        # cada linha fica com todas as de qn ate ao random com todos os pontos
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)     
        res[ix] = np.min(maxd)
    return res
 
def point_dists_mine(base_sets,new_sets):
    """
    return vector of max distances between the base_point (it's only one quaternion rotate)
    and the new_point (all the quaternions)
    """
    res = np.zeros((new_sets.shape[0]))
    for ix in range(len(res)):
        diffs = base_sets[:]-new_sets[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        res[ix] = np.max(dists,axis=-1)
    return res   
    
def spread_quaternions(points,num=100,quats_per_step=100):
    """
    return a spread of num quaternions
    """
    #cria uma matrix de zeros num por 4
    quats = np.zeros((num,4))
    #print quats
    # cria 'num' matrizes, cada uma com points.shape[0] linhas e 3 colunas
    rot_points = np.zeros((num,points.shape[0],3))
    #print rot_points
    #a primeira posição de quats fica =
    quats[0,:] = [0,0,0,1]
    #print quats
    # primeiro conjunto de matrizes fica igual aos points
    rot_points[0,:,:] = points
    #print rot_points
    for ix in range(1,num):
        # criar quats_per_step quaterniões aleatorios 
        rand_quats = random_quaternions(quats_per_step) 
        # fazer a rotação dos pontos usando os quaterniões aleatorios
        positioned = rotate_points(points,rand_quats)
        # ver as distancias (retorna já os mais proximos!)
        dists = point_dists(rot_points[:ix],positioned)
        # ir buscar o maximo das distancias mais proximas
        new_rot = np.argmax(dists)
        
        quats[ix,:]=rand_quats[new_rot,:]
        rot_points[ix,:,:] = positioned[new_rot,:,:]
    #print "number of quaternions: ",len(quats)    
    return quats,rot_points
        
def evaluate(rot_points):
    """
    return array with min distances
    and a structure with the number of quaternion
    closer to him, with quaternios matrices, which matrice with 
    two lines, the first whith the number of the closer quaternion
    (acording to its position on the rot_points)
    and the second line containing that distance
    """
    res = np.ndarray(rot_points.shape[0])
    # estrutura que guarda o quaterniao mais proximo
    # e a distancia entre eles
    bindings = np.zeros((rot_points.shape[0], 2, 1))
    #print "begin evaluate"
    #print res
    for ix in range(len(res)):
        if ix==0:
            base_sets = rot_points[1:]
        elif ix==len(res)-1:
            base_sets = rot_points[:-1]
        else:
            base_sets = np.concatenate((rot_points[:ix],rot_points[ix+1:]))          
        diffs = base_sets[:]-rot_points[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)  
        # nota: maxd contèm as distancias do quaternião presente
        # a todos os outros    
        #res[ix] = np.min(maxd)
        min = 9999
        #refere-se a posicao no rot_points
        quat_number = 0
        for iz in range (0,len(maxd)):
            if maxd[iz] <= min:
                min = maxd[iz]
                if (iz < ix):
                    quat_number = iz
                else:
                    quat_number = iz+1

        bindings[ix,0,0] = quat_number
        bindings[ix,1,0] = min
        res[ix] = min
    return res, bindings
  
def evaluate_no_bindings(rot_points):
    """
    return array with min distances
    """
    res = np.ndarray(rot_points.shape[0])
    for ix in range(len(res)):
        if ix==0:
            base_sets = rot_points[1:]
        elif ix==len(res)-1:
            base_sets = rot_points[:-1]
        else:
            base_sets = np.concatenate((rot_points[:ix],rot_points[ix+1:]))          
        diffs = base_sets[:]-rot_points[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)        
        res[ix] = np.min(maxd)
    return res
    
def normalize_quat(quat):
    mag2 = np.zeros((quat.shape[0]))
    r = np.zeros((quat.shape[0],4),)
    for ix in range(quat.shape[0]):
        #print quat[ix]
        mag2 [ix] = (quat[ix,0] * quat[ix,0]) +  (quat[ix,1] * quat[ix,1]) + (quat[ix,2] * quat[ix,2])+ (quat[ix,3] * quat[ix,3])
        if math.fabs(mag2[ix] - 1.0) > 0.00001:
            mag = math.sqrt(mag2[ix])
            r[ix,0] = quat[ix,0] / mag
            r[ix,1] = quat[ix,1] / mag
            r[ix,2] = quat[ix,2] / mag
            r[ix,3] = quat[ix,3] / mag
    return r
    
def convert_to_quaternions (quat):
    """
    convert points and orientatios to quaternions
    """
    quat[:,:,0]= np.cos(np.radians(quat[:,:,0])/2)
    #quat [:,:,1:] = _normalize(quat [:,:,1:])
    quat [:,:,1] = quat [:,:,1] * np.sin(np.radians(quat[:,:,0])/2)
    quat [:,:,2] = quat [:,:,2] * np.sin(np.radians(quat[:,:,0])/2)
    quat [:,:,3] = quat [:,:,3] * np.sin(np.radians(quat[:,:,0])/2)
    return quat
  
def draw_kde(vals,image_file, band = 0.75):

    me = np.median (vals)    
    av = np.average (vals)    
    var = np.var(vals)
    
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
    
def begin():             
    points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)
    #points = np.array([(0,0,0), (1,1,1),(2,2,2)]).astype(float)
    quaternions_per_set = 100
    number_of_quat = 1000
    #print points
    start_time = time.time()
    quats,rots = spread_quaternions(points,number_of_quat,quaternions_per_set)
    print "elapsed:",time.time()-start_time
    start_time = time.time()
    mins, bindings = evaluate(rots)
    print "elapsed eval:",time.time()-start_time
    
    print bindings
    #print mins
    mediana, av, var = draw_kde(mins,'distribution_'+str(quaternions_per_set)+'.png')
    
    print "Mediana: " , mediana
    print "Media: ", av
    print "Variancia: ", var
    

