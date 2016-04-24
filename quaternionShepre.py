# -*- coding: utf-8 -*-
"""
Normalizar os vetores?
"""

import numpy as np
import  spread_points as sp
import quateriongen as qt


def spread_quat():
	#vamos ter 6624
	# matrix a 3 dimensões
	# vamos ter 288 matrizes, cada uma com 23 quaterniões 
	quatDist = np.zeros((288,23, 4))
	#por defeito faz 288 pontos
	points = sp.GetPointsEquiAngularlyDistancedOnSphere()
	#print points
	
	#Fazer: colocar já os angulos em radianos para melhorar a eficiencia
	angles = np.arange(0,360, 15)
	#print angles
	#i = 0
	for ix in range (0,288):
		quatDist [ix, :,1:] = points[ix,:]
		for v in range(1,24):
			quatDist[ix,v-1,0] = angles[v]
			#print i
			#i = i + 1
			
			
	#print quatDist
	return quatDist
			

	
	
def point_dists(base_sets,new_sets):
    """
    return vector of max distances between each
    new_points to base_ponts
    """
    res = np.zeros(new_sets.shape[0])
    for ix in range(len(res)):
        diffs = base_sets[:]-new_sets[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        res [ix] = np.max(dists,axis=-1)
    return res
	
q = spread_quat()
qu = np.zeros((6624,4))


quat = qt.convert_to_quaternions(q)
#print quat.shape
points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)


# passar de uma matriz a 3 dimensões, para duas dimensões
i = 0
for ix in range (0,288):
	for iz in range (0,23):
		qu [i] = quat [ix, iz,:]
		i = i+1
#print qu.shape


# rodar os pontos usando os novos quaterniões
positioned = qt.rotate_points(points, qu)
#print positioned

mins = qt.evaluate_no_bindings(positioned)
#print mins

qt.draw_kde(mins,'distribution_'+str(6624)+'.png', np.max(mins)/1000)




