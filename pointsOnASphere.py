# -*- coding: utf-8 -*-import math

import math, random

def fibonacci_sphere(N):
	N = float(N) # in case we got an int which we surely got
	pts = []
	
	inc = math.pi * (3-math.sqrt(5))
	off = 2/N
	
	for k in range (0,N):
		y = k * off - 1 + (off / 2)
		r = math.sqrt(1-y*y)
		phi = k * inc
		pts.append([math.cos(phi)*r,y, math.sin(phi)*r])
	return pts
	

	
if __name__ == '__main__':                
    ptsOnSphere = fibonacci_sphere(500, False)    

    #toggle True/False to print them
    if( False ):    
        for pt in ptsOnSphere:  print( pt)

    #toggle True/False to plot them
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