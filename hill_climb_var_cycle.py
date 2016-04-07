# -*- coding: utf-8 -*-
"""
Para melhorar a distribuição, usa-se o hill climbing, mexendo nos
quaternioes aleatoriamente e tentando aumentar ligeiramente a distancia 
ao mais proximo dele, mexendo-se só nas casas decimais

Estruturas:
quaternions: matrix (n,4)
bindings: matirx (n, 2,1) -> n matrizes, cada uma com 2 linhas e uma coluna
		  Cada matriz está ligada com um quaternião n e representa, na primeira
		  linha a posição do quaternião mais proximo, na estrutura quaternioes e a segunda a 
		  distancia entre eles
"""
import math
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import scipy.stats


def random_quaternions(count=100):
    """
    return a matrix with count random quaternions
    each quaternion is a line
    """
	#matrix de count por 3, cheios de numeros aleatorios
    rands = np.random.rand(count,3)
	# todos as posições zero de cada linha
    root_1 = np.sqrt(rands[:,0])
	# equivalente a math.sqrt(1-u1), usando a primeira posição de cada linha
    minus_root_1 = np.sqrt(1-rands[:,0])
    two_pi_2 = np.pi*2*rands[:,1]
    two_pi_3 = np.pi*2*rands[:,2]
    
    res = np.zeros((count,4))
    res[:,0] = minus_root_1*np.sin(two_pi_2)
    res[:,1] = minus_root_1*np.cos(two_pi_2)
    res[:,2] = root_1*np.sin(two_pi_3)
    res[:,3] = root_1*np.cos(two_pi_3)
    
    return res
    
def multiply_quaternions(quats1,quats2):
    """
    return matrix (len,4) for pairwise multiplication of
    quaternions. Matrices quats1 and quats2 must have
    same number of lines and 4 columns
    """
    w1 = quats1[:,0]
    x1 = quats1[:,1]
    y1 = quats1[:,2]
    z1 = quats1[:,3]

    w2 = quats2[:,0]
    x2 = quats2[:,1]
    y2 = quats2[:,2]
    z2 = quats2[:,3]

    res = np.zeros((quats1.shape[0],4))
    
    res[:,0] = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    res[:,1] = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    res[:,2] = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    #res[:,3] = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    res[:,3] = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return res
    
def conjugate(quats):
    """
    return conjugates of quaternions
    """
    res = np.zeros(quats.shape)
    res[:,0]=quats[:,0]
    res[:,1]=-quats[:,1]
    res[:,2]=-quats[:,2]
    res[:,3]=-quats[:,3]
    
    return res
 
def rotate_points(points,quaternions):
    """
    return matrix with rotated points
    points is matrix of points lines and 3 columns
    quaternions is a matrix with quaternion lines and 4 columns
    result is a matrix with (quaternions, points, 3) dimensions
    """
    
    res = np.zeros((quaternions.shape[0],points.shape[0],4))  
    #print res	
    # cada matrix sera igual ao points
    res[:,:,1:] = points   
    #print res	
	# vai buscar os conjugates...
    conjugates = conjugate(quaternions)    
    #print conjugates
    
	# ficamos com o ponto 'rodado' 
    for ix in range(len(points)):
        res[:,ix,:] = multiply_quaternions(quaternions,res[:,ix,:])
        res[:,ix,:] = multiply_quaternions(res[:,ix,:],conjugates)
    return res[:,:,1:]

def point_dists(base_sets,new_sets):
    """
    return vector of max distances between each
    new_points to base_ponts
    """
    res = np.zeros(new_sets.shape[0])
    for ix in range(len(res)):
        diffs = base_sets[:]-new_sets[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1) 	
        res[ix] = np.min(maxd)
    return res
        
def spread_quaternions(points,num=100,quats_per_step=100):
    """
    return a spread of num quaternions
    """
	#cria uma matrix de zeros num por 4
    quats = np.zeros((num,4))
    #print quats
	# cria 'num' matrizes, cada uma com points.shape[0] linhas e 3 colunas
    rot_points = np.zeros((num,points.shape[0],3))
    #print rot_points
	#a primeira posição de quats fica =
    quats[0,:] = [0,0,0,1]
    #print quats
	# primeiro conjunto de matrizes fica igual aos points
    rot_points[0,:,:] = points
    #print rot_points
    for ix in range(1,num):
		# criar quats_per_step quaterniões aleatorios 
        rand_quats = random_quaternions(quats_per_step) 
        #print rand_quats
		# fazer a rotação dos pontos usando os quaterniões aleatorios
        positioned = rotate_points(points,rand_quats)
		# ver as distancias (retorna já os mais proximos!)
        dists = point_dists(rot_points[:ix],positioned)
		# ir buscar o maximo das distancias mais proximas
        new_rot = np.argmax(dists)
		
        quats[ix,:]=rand_quats[new_rot,:]
        rot_points[ix,:,:] = positioned[new_rot,:,:]
    print "number of quaternions: ",len(quats)    
    return quats,rot_points
        
def evaluate(rot_points):
    """
    return array with min distances
	and a structure with the number of quaternion
	closer to him, with quaternios matrices, which matrice with 
	two lines, the first whith the number of the closer quaternion
	(acording to its position on the rot_points)
	and the second line containing that distance
    """
    res = np.ndarray(rot_points.shape[0])
	# estrutura que guarda o quaterniao mais proximo
	# e a distancia entre eles
    bindings = np.zeros((rot_points.shape[0], 2, 1))
    #print "begin evaluate"
    #print res
    for ix in range(len(res)):
        if ix==0:
            base_sets = rot_points[1:]
        elif ix==len(res)-1:
            base_sets = rot_points[:-1]
        else:
            base_sets = np.concatenate((rot_points[:ix],rot_points[ix+1:]))          
        diffs = base_sets[:]-rot_points[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)  
        # nota: maxd contèm as distancias do quaternião presente
		# a todos os outros	
        #res[ix] = np.min(maxd)
        min = 9999

        quat_number = 0
        for iz in range (0,len(maxd)):
            if maxd[iz] <= min:
                min = maxd[iz]
                if (iz < ix):
					quat_number = iz
                else:
	                quat_number = iz+1
        #print "Iteração: ", ix
        #print maxd
        #print res
        bindings[ix,0,0] = quat_number
        bindings[ix,1,0] = min
        res[ix] = min
        #print ligacao
    #print "finais:"
    #print ligacao
    #print res
    return res, bindings
	
def evaluate_no_bindings(rot_points):
    """
    return array with min distances
    """
    res = np.ndarray(rot_points.shape[0])
    for ix in range(len(res)):
        if ix==0:
            base_sets = rot_points[1:]
        elif ix==len(res)-1:
            base_sets = rot_points[:-1]
        else:
            base_sets = np.concatenate((rot_points[:ix],rot_points[ix+1:]))          
        diffs = base_sets[:]-rot_points[ix]
        dists = np.sum(np.square(diffs),axis=-1)
        maxd = np.max(dists,axis=-1)        
        res[ix] = np.min(maxd)
    return res
  
def draw_kde(vals,image_file):

    me = np.median (vals)
    #print "Mediana: " , me
    av = np.average (vals)
    #print "Media: ", av

	
    var = np.var(vals)
    #print "Variancia: ", var
	
	#shapiro wilk test
    #s = scipy.stats.shapiro(vals)
    #print "shapiro: ", s
	
    #k = scipy.stats.kurtosis(vals,axis=0, fisher=False, bias=True)
    #print "kurtosis: ", k
	
    kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(vals[:,np.newaxis])
    plt.figure(figsize=(12,8))
    xs = np.linspace(0, max(vals)*1.2, 1000)[:, np.newaxis]
    ys = np.exp(kde.score_samples(xs))
    plt.plot(xs,ys,'-b', linewidth=3)
    plt.savefig(image_file,dpi=300,bbox_inches='tight')
    plt.close()
    return me, var, av
	
def point_dists_mine(base_sets,new_sets):
	"""
	return vector of max distances between each
	new_points to base_ponts
	"""
	res = np.zeros(new_sets.shape[0])
	for ix in range(len(res)):
		#dists = dist(base_sets, new_sets[ix])
		#print "distancia do ponto o"dists
		diffs = base_sets[:]-new_sets[ix]
		dists = np.sum(np.square(diffs),axis=-1)
		res[ix] = np.max(dists,axis=-1)
	return res

def hill_climbing(quaternions, bindings, mediana, points, rot_points, variancia, av):
	print "\nHill climbing"
	#vamos sempre trabalhar com os quaternioes antigos, e guardar nas estrutras novas!
	# estava a mudar so o apontador... (afinal é java...)

	new_set_quat = np.copy(quaternions)
	new_rot_points = np.copy(rot_points)
	to_much = 2
	#print bindings
	#print "length = ", bindings.shape[0]
	#print mediana
	it = 0
	accepted = 0
	var = np.copy(variancia)
	start_time = time.time()
	#while ( (variancia < var -1) or (it < number_it)):
	while ( it < number_it):
		for ix in range (0,bindings.shape[0]):
			# só queremos alterar alqueles que estão muito proximos
			a = bindings[ix, 1,0]

			#print mediana
			if  (a < mediana):
				#print "distancia a aumentar: ", a
				# arranjar randons
				randoms = np.random.uniform(-1,1,(number_of_randoms,4))
				# temos de mexer pouco nos quaternioes
				randoms = np.divide(randoms, value_to_divide)
				#print randoms
				#print "getting the: ", bindings[ix,0,0], " quaternion"
				#print "value: ", quaternions[bindings[ix,0,0]]
				news_quats = np.sum((randoms, quaternions[bindings[ix,0,0]]))
				#print news_quats
				new_points = rotate_points(points, news_quats)
				#print "old point:"
				#print rot_points[bindings[ix,0,0]]
				#print "novos pontos:"
				#print new_points
				dist = point_dists_mine(rot_points[ix], new_points)
				#print "distancias"
				#print dist
				# no futuro usar todos os valores
				#dist = np.where( dist > mediana )  --> não se pode usar pois é necessario saber a posicao do quaterniao que gerou estes valores
				#print dist
				for iz in range (len(dist)):
					if (dist[iz] > a) & (dist[iz] < (mediana + to_much)):
						#guardar os novos pontos
						#print "Novo ponto: ", iz
						new_rot_points[bindings[ix,0,0]] = new_points[iz]
						#print "Pontos antigos: "
						#print rot_points[bindings[ix,0,0]]
						#print "Novos pontos: "
						#print new_rot_points[bindings[ix,0,0]]
						#guardar o novo quaterniao
						new_set_quat[bindings[ix,0,0]] = news_quats[iz]
						#print "Nova distancia = ", dist[iz]
						#print "Novo quaterniao = ", news_quats[iz]
						#break;
		
		
		
		mins = evaluate_no_bindings(new_rot_points)
		var_old = np.copy(var)
		varTemp = np.var(mins)
		#print "Variancia antiga: ", var_old
		#print "Variancia nova: ", varTemp
		it = it +1
		#if (varTemp*100 < var_old*100):
		if ((varTemp-var_old) < 0.):
			#print var-var_old
			rot_points = np.copy(new_rot_points)
			quaternions = np.copy(new_set_quat)
			var = np.copy(varTemp)
			accepted = accepted + 1
		else:
			var = np.copy(var_old)
		#print "Variancia aceite: ", var, "\n"
	
	#mins, bindings = evaluate(rot_points)
	#mediana2, var2 = draw_kde(mins,'distribution_new_'+str(quaternions.shape[0])+'.png')
	#print "Mediana antiga: ", mediana, " mediana nova: ", mediana2
	#print "Variancia antiga: ", var, " Variancia nova: ", var2
	
	mins = evaluate_no_bindings(rot_points)
	mediana2, var2, av2 = draw_kde(mins,'distribution_new_'+str(quaternions.shape[0])+'.png')
	#print "Mediana antiga: ", mediana, " mediana nova: ", mediana2, " diferença: ", math.fabs(mediana-mediana2)
	#print "Media antiga: ", av, " media nova: ", av2, " diferença: ", math.fabs(av-av2)
	print "Variancia antiga: ", variancia, " Variancia nova: ", var2, " diferença: ", var2-variancia
	print "numero de aceitações: ", accepted
	print "elapsed:",time.time()-start_time
	#print "Pontos antigos: "
	#print rot_points
	#print "Novos pontos: "
	#print new_rot_points
	
	
	#return new_set_quat, new_rot_points
	return var2-variancia, accepted
    
            
points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)
#points = np.array([(0,1,0), (1,1,1),(2,2,2)]).astype(float)
# variavies globais para alterar
quaternions_per_set = 100
number_of_quat = 4000
#para o hill climbing
value_to_divide = 1000
number_of_randoms = 100
number_it = 20
#print points
vdg = 0
acg = 0
start_time_global = time.time()
for times in range (0,3):
	start_time = time.time()
	quats,rots = spread_quaternions(points,number_of_quat,quaternions_per_set)
	print "elapsed:",time.time()-start_time
	start_time = time.time()
	mins, bindings = evaluate(rots)
	print "elapsed eval:",time.time()-start_time
	#print mins
	mediana, var, av = draw_kde(mins,'distribution_'+str(number_of_quat)+'.png')
	#print "Media: ", av
	#print "Mediana: ", mediana
	#print "Variancia: ", var
#print quats
	
	vd, a = hill_climbing(quats, bindings, mediana, points, rots, var, av)
	
	
	
	if times == 0:
		vdg = vd
		acg = a
	else:
		vdg = (vd + vdg)/2
		acg = (a + acg)/2
	
	print "\n"
print "divide by: ", value_to_divide
print "iterações: ", number_it
print "randoms: ", number_of_randoms
print "Var Dif: ", vdg
print "Ace Dif: ", acg
print "elapsed eval global:",time.time()-start_time_global
print "\n\n\n"