# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 17:31:08 2016

@author: Moncada
"""

import quateriongen as qt
import numpy as np


def avaliate(points_quat_opt):


    points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)

    randoms = qt.random_quaternions(5000)


    points_random = qt.rotate_points(points, randoms)
    
    min_dist = qt.point_dists(points_quat_opt, points_random)
    
    max_d = np.max(min_dist)
    return max_d
    #print "distancia maxima: ",max_d
