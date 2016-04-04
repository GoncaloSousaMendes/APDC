# -*- coding: utf-8 -*-
"""
Para melhorar a distribuição, usa-se o hill climbing, mexendo nos
quaternioes aleatoriamente e tentando aumentar ligeiramente a distancia 
ao mais proximo dele, mexendo-se só nas casas decimais
"""
import math
import numpy as np

def dist (p1, p2):
	return scipy.spatial.distance.cdist(p1,p2)

def hill_climbing(quaternions, bindings, mediana):
	for ix in range (len(bindings)):
		# arranjar randons
		randoms = np.random.uniform(-1,1,(10,4))
		# new quaternions c = np.sum((a,b))
		new_quat = np.sum((randoms, quaternions[bindings[ix,0,:]]))
		
		