"""
Retirado de:
http://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
"""

from math import cos, sin, pi, sqrt

def GetPointsEquiAngularlyDistancedOnSphere(numberOfPoints=45):
    """ each point you get will be of form 'x, y, z'; in cartesian coordinates
        eg. the 'l2 distance' from the origion [0., 0., 0.] for each point will be 1.0 
        ------------
        converted from:  http://web.archive.org/web/20120421191837/http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere ) 
    """
    dlong = pi*(3.0-sqrt(5.0))  # ~2.39996323 
    dz   =  2.0/numberOfPoints
    long =  0.0
    z    =  1.0 - dz/2.0
    ptsOnSphere =[]
    for k in range( 0, numberOfPoints): 
		r    = sqrt(1.0-z*z)
		ptNew = (cos(long)*r, sin(long)*r, z)
		ptsOnSphere.append( ptNew )
		z    = z - dz
		long = long + dlong
		# so queremos em metade da esfera
		#if(k == 288):
		#	break
    return ptsOnSphere


	
	

if __name__ == '__main__':                
    ptsOnSphere = GetPointsEquiAngularlyDistancedOnSphere(500)    

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