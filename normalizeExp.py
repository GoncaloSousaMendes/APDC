# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:42:58 2016

@author: Moncada

normalize quanternions with numpy
"""

import numpy as np
import math

def normalize_quat(quat):
    mag2 = np.zeros((quat.shape[0]))
    r = np.zeros((quat.shape[0],4),)
    for ix in range(quat.shape[0]):
        #print quat[ix]
        mag2 [ix] = (quat[ix,0] * quat[ix,0]) +  (quat[ix,1] * quat[ix,1]) + (quat[ix,2] * quat[ix,2])+ (quat[ix,3] * quat[ix,3])
        print mag2[ix]
        if math.fabs(mag2[ix] - 1.0) > 0.00001:
            mag = math.sqrt(mag2[ix])
            r[ix,0] = quat[ix,0] / mag
            r[ix,1] = quat[ix,1] / mag
            r[ix,2] = quat[ix,2] / mag
            r[ix,3] = quat[ix,3] / mag
    return r
    


        
    
    
def test():
    quat = np.zeros((5,4))
    quat[0,:] = [1,0,1,0]
    quat[1,:] = [0,1,0,1]
    
    quat[2,:] = [1,1,0,1]
    quat[3,:] = [0,1,1,1]
    quat[4,:] = [1,1,1,1]
    
    
    
    
    
    r = normalize_quat(quat)
    
    print r