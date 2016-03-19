# -*- coding: utf-8 -*-

import numpy as np
import time

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
    # cada matrix sera igual ao points
    res[:,:,1:] = points   
	# vai buscar os conjugates...
    conjugates = conjugate(quaternions)    
    
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
        diffs = base_sets[:]-new_sets[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)        
        res[ix] = np.min(maxd)
    return res
        
    
    
def spread_quaternions(points,num=100,quats_per_step=100):
    """
    return a spread of num quaternions
    """
	#cria uma matrix de zeros num por 4
    quats = np.zeros((num,4))
	# cria num matrizes, cada uma com points.shape[0] linhas e 3 colunas
    rot_points = np.zeros((num,points.shape[0],3))
	#a primeira posição de quats fica =
    quats[0,:] = [0,0,0,1]
	# primeiro conjunto de matrizes fica igual aos points
    rot_points[0,:,:] = points
    for ix in range(1,num):
		# criar quats_per_step quaterniões aleatorios 
        rand_quats = random_quaternions(quats_per_step) 
		# fazer a rotação dos pontos usando os quaterniões aleatorios
        positioned = rotate_points(points,rand_quats)  
		# ver as distancias
        dists = point_dists(rot_points[:ix],positioned)
		# ir buscar o maximo das distancias mais proximas
        new_rot = np.argmax(dists)
		
        quats[ix,:]=rand_quats[new_rot,:]
        rot_points[ix,:,:] = positioned[new_rot,:,:]
        
    return quats
        
points = np.array([(0,0,0),(3,3,3), (3,3,0),(3,0,0),(0,3,0), (0,0,3), (0,3,3), (3,0,3)]).astype(float)
#print points
start_time = time.time()
quats = spread_quaternions(points,1000,100)
print "elapsed:",time.time()-start_time
#print quats