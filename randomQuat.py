import math
import random
import quaternion

"""
 Function that generates uniforms, random quaternions
"""
def generate_random_quaternion():
	u1 = random.random()
	u2 = random.random()
	u3 = random.random()
	
	w = math.sqrt(1-u1)*math.sin(2*math.pi*u2)
	x = math.sqrt(1-u1)*math.cos(2*math.pi*u2)
	y = math.sqrt(u1)*math.sin(2*math.pi*u3)
	z = math.sqrt(u1)*math.cos(2*math.pi*u3)
	v = x,x,y,z
	return v
	
	

"""
Function that give us the vector 
and angle of a quaternion, in degrees
"""	
def generate_randoms(times):
	maxAngle = 0
	minAngle = 360
	maxDist = 0
	quatOfMAx = (0,0,0,0)
	point = (1,1,1)
	for i in range (0, times):
		random = generate_random_quaternion()
		result = quaternion.qv_mult(random, point)
		
		from scipy.spatial import distance
		dst = distance.euclidean(point,result)
		
		#test for the max and min angle we got
		vector = get_vector_from_quat(random)
		
		if vector [0] < minAngle:
			minAngle = vector[0]
			
		elif vector[0] > maxAngle:
			maxAngle = vector[0]
		
		if maxDist < dst:
			maxDist = dst
			quarOfMax = vector
			
	print("maxAngle: ", maxAngle)
	print("minAngle: ", minAngle)
	print("distance: ", maxDist)
	print("vector used: ", vector)

def test_getting_vetor():
	# expected: angle = 90, axis = 1,0,0
	q = [0.7071, 0.7071, 0, 0]
	v = get_vector_from_quat(q)
	print (v)
	q = quaternion.axisangle_to_q([1,0,0], math.radians(90))
	print (q)
	v = get_vector_from_quat(q)
	print (v)

def test_for_random():
	q = generate_random_quaternion()
	vector = get_vector_from_quat(q)
	
def test_for_dist():
	point = (1,1,1)
	q = quaternion.axisangle_to_q([1,0,0], math.radians(360))
	result = quaternion.qv_mult(q, point)
	from scipy.spatial import distance
	dst = distance.euclidean(point,result)
	
	print(dst)
	
	
	
	