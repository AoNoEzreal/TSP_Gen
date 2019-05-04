# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:13:51 2019

@author: ybett
"""
import csv
import math
import itertools
import time
import random

class path:
    def __init__(self,order,fitness = 0,length=0):
        self.order = order #Order represente le chemin I.E un tuple de chiffres uniques allant de 1 à n
        self.fitness = fitness
        self.length = length
    

def init():
    nb = 0
    results = []
    with open('data/test10.csv','r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if(nb == 0):
                nb += 1 # On convertit le premier element en entier
            else :
                results.append(row)

        for i in range(0,len(results)):
            for j in range(0,len(results[i])):
                results[i][j] = float(results[i][j]) # On passe tout en float
    return results

def distance(x1,y1,x2,y2):
    #print('x1 = ',x1,' y1 = ', y1,' x2 = ', x2, ' y2 = ',y2)
    d = abs(math.sqrt(((x1-x2)**2) + ((y1-y2)**2)))
    return d

def compute_Dist_Matrix(data,combi): #Calcule la matrice des distances data = coordonnées des points combi : liste de combinaisons de 2 elements générées
    DistMatrix = {}
    for pair in combi:
        x1 = data[pair[0]][0]
        y1 = data[pair[0]][1]
        x2 = data[pair[1]][0]
        y2 = data[pair[1]][1]
        x = pair[0]
        y = pair[1]
        DistMatrix[x,y] = distance(x1,y1,x2,y2)
        DistMatrix[y,x] = DistMatrix[x,y]
    return DistMatrix

def populate(nb,cpt): #nb = combiens de points dans un chemin et cpt = nombre d'individus qu'on veut generer
    a = range(1,nb)
    population = []
    for i in range(0,cpt):
        population.append(path(random.sample(a,nb-1))) # genere des populations aléatoires de nb-1 elements
    
    return list(population)

def testPopulation(dists,population):
    best = path((1),0,999999999) #On initialise notre meilleur element avec une longeur très grande
    p1 = 0
    p2 = 0
    for i in range(0,len(population)):
        first = population[i].order[0] # Le premier point (suivant le point 0)
        tot = 0
        for j in range(0,len(population[i].order)-1):
            p1 = population[i].order[j]
            p2 = population[i].order[j+1]
            tot = tot + dists[p1,p2]

        tot += dists[p2,0] + dists[0,first] # On ajoute le départ depuis le point 0 et le retour au point 0
        population[i].length = tot
        population[i].fitness = (1/(tot+1)) # On ajoute 1 au dénominateur au cas ou la 
        #                                   distance serait nulle ( impossible sauf si tout les points sont superposés mais au cas ou)
        if(tot<best.length):
            best = population[i]
    return best

# def normaliseFitness(population): #pour donner plus de sens à notre critere on le rapporte à un nombre entre 0 et 1 
#     somme = sum(path.fitness for path in population) #La somme de tous les criteres doit être égale à 1 donc on la calcule
    
#     for i in range(0,len(population)):
#         population[i].fitness = population[i].fitness/somme

def Pick(population):
    somme = sum(path.fitness for path in population)
    # print(list(path.fitness for path in population))
    # print(math.floor(somme))
    r = random.randrange(start=0,stop=math.ceil(somme))
    running_sum = 1

    for path in population:
        running_sum += path.fitness
        if r < running_sum:
            return path

def permuts(nb): #Fonction qui initialise une liste contenant tout les chemins possibles là pour tester uniquement
    pop = []
    perms =  list(itertools.permutations(range(1,nb)))
    for perm in perms:
        pop.append(path(perm))
    return pop

# def pickOne(population):
#     index = 0
#     r = random.uniform(0,1)
#     normaliseFitness(population)
#     try:
#         while (r > 0):
#             #print(index)
#             r = r - population[index].fitness # on va retirer la probabilité de l'element tiré 
#             index +=1 
#     except IndexError:
#         print('error out of range ',index)
#         print(list(path.fitness for path in population))
#         print(r)
#         exit()
#     index -=1 # si on a trouvé le bon element, index est incrementé une fois de trop alors on décremente pour avoir le bon element
#     return population[index]

def mutate(indiv):
    idx = range (len(indiv.order))
    i1,i2 = random.sample(idx,2)
    indiv.order[i1],indiv.order[i2] = indiv.order[i2],indiv.order[i1] #mutation basique pour l'instant
    return indiv

def nextGen(population):
    newPopulation = []
    for i in range(0,len(population)):
        pick = Pick(population)
        mutant = mutate(pick)
        newPopulation.append(mutant)
    return newPopulation

# def sortPopulation(population):
#     return sort
start = time.time()
data = init()
#population = permuts(10)
population = populate(10,1000)
#print(list(path.order for path in population))
combinaisons = (list(itertools.combinations(range(0,10),2)))
distMatrix = compute_Dist_Matrix(data,combinaisons)
# best = testPopulation(distMatrix,population)
# normaliseFitness(population)
# print(best.length)
# print(best.order)
# print(best.fitness)
# newPop = nextGen(population)
# best = testPopulation(distMatrix,newPop)
# print(best.length)
# print(best.order)
# print(best.fitness)

bestsOfGen = []
for i in range(500):
    #print(i)
    best = testPopulation(distMatrix,population)
    #normaliseFitness(population)
    bestsOfGen.append(best.length)
    newPop = nextGen(population)
    population = newPop[:]

print(min(bestsOfGen))


# for()