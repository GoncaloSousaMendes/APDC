#!/usr/bin/python
# coding: latin-1
import os, sys
"""
 This script works with quaternions
 it perfoms the multiplication, conversion (from and to quaternion)
 and create random quaternions
"""
import math
import random


""" 
 Program that computes de point resulting of a roation
 using quaternions
 it recieves:
 - a point, on the form (w,x,y,z), where w is 0
 - a vetor, on the form (w,x,y,z)
 - an angle in degrees
"""
def calc_quaternion(point, vector, angle):
	angle = math.radians(angle)
	r1 = axisangle_to_q(vector, angle)
	q = qv_mult(r1,point)
	return q
	
	
# translate de vector and the angle to quaternion
def axisangle_to_q(v, theta):
	v = normalize(v)
	x, y, z = v
	theta /= 2

	w = math.cos(theta)
	x = x * math.sin(theta)
	y = y * math.sin(theta)
	z = z * math.sin(theta)

	return w, x, y, z
	
"""
 perfom the aritmetics of p' = qpq'
 when p is a point, or a 'pure' quaternion (w=0)
"""	
def qv_mult(q1, v1):
	q2 = (0.0,) + v1
	#qq = q_mult(q1,q2)
	#print qq
	#qqq = q_conjugate(q1)
	#print qqq
	#return q_mult(qq, qqq)
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

"""
 perfom the aritmetics of p' = qpq'
 when p is another quaternion
"""	
def qv_mult2Quat(q1,q2):
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]
	
# caculatethe conjugate
def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)
	
# the hamilton method to operate on complex numbers
def q_mult(q1, q2):
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2
	w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
	x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
	y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
	z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    #z = w1 * z2 + z1 * w2 - y1 * x2 + x1 * y2 
	return w, x, y, z

# to normalize the vectors	
def normalize(v, tolerance=0.00001):
	mag2 = sum(n * n for n in v)
	if abs(mag2 - 1.0) > tolerance:
		mag = math.sqrt(mag2)
		v = tuple(n / mag for n in v)
	return v
	
	
	
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
def get_vector_from_quat(quaternion):
	qw,qx,qy,qz = quaternion
	if qw > 1:
		quaternion.normalize(quaternion)
	qw,qx,qy,qz = quaternion	
	angle = 2*math.acos(qw)
	angle = math.degrees(angle)
	s = math.sqrt(1-qw*qw)
	if s < 0.001:
		x = qx
		y = qy
		z = qz
	else:
		x = qx/s
		y = qy/s 
		z = qz/s 
	vector = angle, x, y, z
	return vector
	
	

"""
The output should be equal to the input 
"""	
def test():
	
	"""
	curiosidade: 
	se passarmos os angulos ((math.pi*2)/3), ou 120graus, o resultado sera o mesmo
	mas, noutras experiencias vemos que o que interessa e o angulo em radianos,
	Aqui passmos em graus, pois está implementada uma funcao que converte para radianos
	teste
	angle = ((math.pi*2)/3)
	vector = (1, 0, 0)
	angle = 360
	point = (1,1,1)
	point = calc_quaternion(point, vector, angle)
	
	vector = (0, 1, 0)
	point = calc_quaternion(point, vector, angle)
	
	vector = (0, 0, 1)
	point = calc_quaternion(point, vector, angle)
	
	vector = (1,0,0)
	angle = 90
	
	v = axisangle_to_q(vector, angle)
	print (v)
	
	
	angle = ((math.pi*2)/3)
	vector = (1, 0, 0)
	angle = 360
	point = (1,1,1)
	point = calc_quaternion(point, vector, angle)
	
	vector = (0, 1, 0)
	point = calc_quaternion(point, vector, angle)
	
	vector = (0, 0, 1)
	point = calc_quaternion(point, vector, angle)
	
	print(point)
	"""
	vector = (1, 1, 1)
	angle = 120
	point = (1,0,0)
	point = calc_quaternion(point, vector, angle)
	
	print point
	
	
	

	
