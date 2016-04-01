# -*- coding: utf-8 -*-

import math
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
	
	#colocar já os angulos em radianos para melhorar a eficiencia
	angles = np.arange(0,360, 15)
	#print angles
	for ix in range (0,288):
		quatDist [ix, :,1:] = points[ix,:]
		for v in range(0,23):
			quatDist[ix,v,0] = angles[v]
			
			
	#print quatDist
	return quatDist
	
	
	
def _convert_to_quaternions (quat):
	quat[:,:,0]= np.cos(np.radians(quat[:,:,0])/2)
	#quat [:,:,1:] = _normalize(quat [:,:,1:])
	quat [:,:,1] = quat [:,:,1] * np.sin(np.radians(quat[:,:,0])/2)
	quat [:,:,2] = quat [:,:,2] * np.sin(np.radians(quat[:,:,0])/2)
	quat [:,:,3] = quat [:,:,3] * np.sin(np.radians(quat[:,:,0])/2)
	return quat
	
	
# to normalize the vectors		
def _normalize(v, tolerance=0.00001):
	mag2 = sum(n * n for n in v)
	if abs(mag2 - 1.0) > tolerance:
		mag = math.sqrt(mag2)
		v = tuple(n / mag for n in v)
	return v	
	
	
q = spread_quat()
quat = _convert_to_quaternions(q)
points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)

# rodar os pontos usando os novos quaterniões
positioned = qt.rotate_points(points, quat)
#
dists = qt.point_dists(rot_points[:ix],positioned)



