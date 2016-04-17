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

import numpy as np
import time
import quateriongen as qt


def hill_climbing(quaternions, bindings, mediana, points, rot_points, variancia, av):
    print "\nHill climbing"
    #vamos sempre trabalhar com os quaternioes antigos, e guardar nas estrutras novas!

    new_set_quat = np.copy(quaternions)
    new_rot_points = np.copy(rot_points)
    to_much = 2
    it = 0
    accepted = 0
    var = np.copy(variancia)
    start_time = time.time()
    while ( it < number_it):
        for n_q in range (0, bindings.shape[0]):
            # só queremos alterar alqueles que estão muito proximos
            a = bindings[n_q, 1,0]
            #print mediana
            if  (a < mediana):
                # arranjar randons
                randoms = np.random.uniform(-1,1,(number_of_randoms,4))
                # temos de mexer pouco nos quaternioes
                randoms = np.divide(randoms, value_to_divide)
                
                news_quats = np.sum((randoms, quaternions[bindings[n_q,0,0]]))
                news_quats = qt.normalize_quat(news_quats)
    
                new_points = qt.rotate_points(points, news_quats)
               
                dist = qt.point_dists_mine(rot_points[n_q], new_points)

                for iz in range (len(dist)):
                    if (dist[iz] > a) & (dist[iz] < (mediana + to_much)):
                        #guardar os novos pontos
                        new_rot_points[bindings[n_q,0,0]] = new_points[iz]
                        #guardar o novo quaterniao
                        new_set_quat[bindings[n_q,0,0]] = news_quats[iz]
                        if stop_at_first == 1:
                            break;
        
        
        
        mins = qt.evaluate_no_bindings(new_rot_points)
        var_old = np.copy(var)
        varTemp = np.var(mins)
        it = it +1
        if ((varTemp-var_old) < 0.):
            rot_points = np.copy(new_rot_points)
            quaternions = np.copy(new_set_quat)
            var = np.copy(varTemp)
            accepted = accepted + 1
        else:
            var = np.copy(var_old)
    

    
    mins = qt.evaluate_no_bindings(rot_points)
    mediana2, var2, av2 = qt.draw_kde(mins,'distribution_new_'+str(quaternions.shape[0])+'.png', 0.75)
    print "Variancia antiga: ", variancia, " Variancia nova: ", var2, " diferença: ", var2-variancia
    print "numero de aceitações: ", accepted
    print "elapsed:",time.time()-start_time

    return var2-variancia, accepted
  

 
            
points = np.array([(0,0,0),(6,9,3), (6,9,0),(6,0,0),(0,9,0), (0,0,3), (0,9,3), (6,0,3)]).astype(float)

# variavies globais para alterar
quaternions_per_set = 100
number_of_quat = 100
#para o hill climbing
value_to_divide = 1000
number_of_randoms = 100
number_it = 10
stop_at_first = 0
#print points
vdg = 0
acg = 0
start_time_global = time.time()
for times in range (0,1):
    start_time = time.time()
    quats,rots = qt.spread_quaternions(points,number_of_quat,quaternions_per_set)
    print "elapsed:",time.time()-start_time
    start_time = time.time()
    mins, bindings = qt.evaluate(rots)
    print "elapsed eval:",time.time()-start_time

    mediana, av, var = qt.draw_kde(mins,'distribution_'+str(number_of_quat)+'.png')

    
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