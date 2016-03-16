"""
this script will generate random quaternions
and atempt to uniform the distribution
"""

import math
import quaternion
import time
from scipy.spatial import distance
from sys import maxsize


def uni_quat():
	# the points to test
	points = _generatePoints()
	# group where we're gonna store the quaternions generated with uniform
	# distribution 
	quatGroup = []
	#the first quaternion
	q = quaternion.generate_random_quaternion()
	quatGroup.append(q)
	start_timeP = time.time()
	for i in range (49):
		# generate more random and calculate the distance do quatGroup
		#randomQuat = ()
		maxDistQuat = 0
		quatToAdd = None
		for j in range (30):
			r = quaternion.generate_random_quaternion()
			#para cada quaterniao no quatGroup vamos ver qual a sua distancia o quaterniao r
			min_of_all_dst = maxsize
			for q in quatGroup:
				dst_to_q = _calculateDistQuat(q,r,points)
				# ficamos com a distancia entre o nosso random e um quaterniao
				# do quatGroup (ou seja, do R)
				# se a distancia entre o random e o quaterniao q for menor
				# do que já temos, ficamos com ela
				if dst_to_q < min_of_all_dst:
					min_of_all_dst = dst_to_q
					
			
			
	
			# temos de guardar o quaterniao que tem a maior distancia, entre os que estão mais perto, para R (quatGroup)
			if min_of_all_dst > maxDistQuat:
				maxDistQuat = min_of_all_dst
				quatToAdd = r
				
		#print("adding", quatToAdd)
		quatGroup.append(quatToAdd)

		
	elapsed_timeP = time.time() - start_timeP
	print ("time for generating R = ", elapsed_timeP)
	print(len(quatGroup), "\n")
	
	
	# avaliar a distribuição de R
	start_timeP = time.time()
	_avaliateQualaty(quatGroup, points)
	elapsed_timeP = time.time() - start_timeP
	print ("\ntime for analise R = ", elapsed_timeP)

"""
 Função para avaliar a qualidade da distribuição dos quaterniões
"""	
def _avaliateQualaty(quatGroup, points):
	mediaMin = 0
	minDist = maxsize
	#print(minDist)
	listForPrint = []
	for i in range (0,len(quatGroup)):
		# retirar o ultimo da lista (para ele não se comparar a si proprio) 
		# para comparar com os outros todos e descobrir o mais proximo
		quat = quatGroup.pop()
		# para ver se há repetidos, so para testes, devem ser 0!
		c = quatGroup.count(quat)
		if c != 0:
			print("existem ", c, " iguais")
		#print ("existem ",c, " quaterniões iguas ao que retiramos")
		minDstQuat = maxsize
		for q in quatGroup:
			dst = _calculateDistQuat(quat, q, points)
			#queremos o mais proximo para este quaternião 
			if dst < minDstQuat:
				minDstQuat = dst
				
		# vamos saber qual a distancia mais pequena entre todos os quaterniões
		if minDstQuat < minDist:
			minDist = minDstQuat
	
		# vamos guardar para cada quaternião a sua distancia ao mais proximo
		listForPrint.append((quat, minDstQuat))
		# inserimos a na cabeça da lista o que retiramos
		quatGroup.insert(0, quat)
		if i == 0:
			mediaMin = minDstQuat
		else:
			mediaMin = (mediaMin + minDstQuat)/2
			
		
	t = 1
	for q in listForPrint:
		print( t, ": ", q[1])
		t = t+1
		
	print("media: ", mediaMin)
	print("menor distancia: ", minDist)

"""
 Função que calcula a distancia entre dois quaterniões
"""	
def _calculateDistQuat (q, r, points):
	maxDst = 0
	#start_timeP = time.time()
	# para cada ponto do nosso objecto:
	for po in points:
		pointInR = quaternion.qv_mult(q, po)
		pointInM = quaternion.qv_mult(r, po)
		# NOTA: VER DISTANCIAS NEGATIVAS!!!
		dst = distance.euclidean(pointInR,pointInM);
		# se a nova distancia for maior que a anterior, ficamos com ela
		if abs(dst) > maxDst:
			maxDst = abs(dst)

		
	#elapsed_timeP = time.time() - start_timeP
	#print ("time for all ppints = ", elapsed_timeP)
	return maxDst
		
def _generatePoints():
	return [(0,0,0),(3,3,3), (3,3,0),(3,0,0),(0,3,0), (0,0,3), (0,3,3), (3,0,3)]
	 
	
