# -*- coding: utf-8 -*-

import math
import numpy as np

def dist (p1, p2):
	return scipy.spatial.distance.cdist(p1,p2)

def hill_climbing(quaternions, mins):
	for ix in range (len(quaternions)):
		