"""
Retirado de:
http://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
Contem duas maneiras de espalhar pontos por uma esfera:
 - metodo de Saff and Kuijlaars
 - metodo de fibonacci
"""

from math import cos, sin, pi, sqrt
import random
import numpy as np

# metodo de Saff and Kuijlaars
# http://web.archive.org/web/20120421191837/http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere
def GetPointsEquiAngularlyDistancedOnSphere(numberOfPoints=576):
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
    ptsOnSphere =[]
    for k in range( 0, numberOfPoints): 
		r = sqrt(1.0-z*z)
		ptNew = (cos(long)*r, sin(long)*r, z)
		ptsOnSphere.append( ptNew )
		points[k] = ptNew
		z    = z - dz
		long = long + dlong
		# so queremos em metade da esfera
		if(k == 287):
			break
    return points

	
def fibonacci_sphere(samples=1,randomize=True):
	rnd = 1.
	if randomize:
		rnd = random.random() * samples
	
		
	points = []
	offset = 2./samples
	increment = pi * (3. - sqrt(5.));


	for i in range(samples):
		y = ((i * offset) - 1) + (offset / 2);
		r = sqrt(1 - pow(y,2))
	
		phi = ((i + rnd) % samples) * increment
		
		x = cos(phi) * r
		z = sin(phi) * r
		
		points.append([x,y,z])
		
		if i == 288:
			break

	return points

if __name__ == '__main__':                
	#ptsOnSphere = fibonacci_sphere(500, False)  
    ptsOnSphere = GetPointsEquiAngularlyDistancedOnSphere(576)
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

        for pt in ptsOnSphere:
            x_s.append( pt[0]); y_s.append( pt[1]); z_s.append( pt[2])

        ax.scatter3D( array( x_s), array( y_s), array( z_s) )                
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
        p.show()
        #end