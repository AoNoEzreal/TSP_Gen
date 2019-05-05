# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:13:51 2019

"""
import csv
import math
import itertools
import time
import random
import copy
#faire les bébés et ajouter l'élite de la nation
random.seed()
class path:
    def __init__(self,order,fitness = 0,length=0):
        self.order = order #Order represente le chemin I.E une liste de chiffres uniques allant de 1 à n
        self.fitness = fitness # la fitness et 1/(1+length) plus la distance est grande plus la fitness est petite moins ce chemin a de chances d'être selectionné
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
        first = population[i].order[0] # Le premier point (après le point 0)
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

def normalizeFitness(population): #On transforme notre critere en probabilité comprise entre 0 et 1
    maximum = max(path.fitness for path in population) 
    
    for i in range(0,len(population)):
        population[i].fitness = population[i].fitness/maximum

def Pick(population): # Ne fonctionne qu'avec une population >= 100
    somme = sum(path.fitness for path in population)
    # print(list(path.fitness for path in population))
    # print(math.floor(somme))
    r = random.randrange(start=0,stop=math.floor(somme))
    running_sum = 1
    for path in population:
        running_sum += path.fitness
        if r < running_sum:
            choosenOne = copy.deepcopy(path)
            return choosenOne

def permuts(nb): #Fonction qui initialise une liste contenant tout les chemins possibles là pour tester uniquement
    pop = []
    perms =  list(itertools.permutations(range(1,nb)))
    for perm in perms:
        pop.append(path(perm))
    return pop

def pickOne(population):
    index = 0
    r = random.uniform(0,1)
    #normaliseFitness(population)
    try:
        while (r > 0):
            #print(index)
            r = r - population[index].fitness # on va retirer la probabilité de l'element tiré 
            index +=1 
    except IndexError:
        print('error out of range ',index)
        print(list(path.fitness for path in population))
        print(r)
        exit()
    index -=1 # si on a trouvé le bon element, index est incrementé une fois de trop alors on décremente pour avoir le bon element
    choosenOne = copy.deepcopy(population[index])
    return choosenOne

def pickOneHatem(population):
    r = random.uniform(0,1)
    for indiv in population:
        if indiv.fitness > r:
            return indiv

def mutate(indiv,mutationRate):
    choosenOne = copy.deepcopy(indiv) #On évite les problemes de reférence
    r = random.uniform(0,1)
    if(r < mutationRate):
        idx = range (len(choosenOne.order))
        i1,i2 = random.sample(idx,2)
        choosenOne.order[i1],choosenOne.order[i2] = choosenOne.order[i2],choosenOne.order[i1] #mutation basique pour l'instant
    return choosenOne

# def mutatePopulation(population,mutationRate):
#     mutatedPopulation = []

#     for i in range(0,len):


def selection(population,eliteSize): #La population doit être triée par fitness au préalable
    newPopulation = []
    for i in range(0,eliteSize):
        eliteIndiv = copy.deepcopy(population[i])
        newPopulation.append(eliteIndiv)
    for i in range(0,len(population)-eliteSize):
        pick = pickOne(population)
        newPopulation.append(pick)
    return newPopulation

def sortPopulation(population):
    return  sorted(population,key=lambda x: x.fitness,reverse = True)

def breeding(p1,p2):
    child = path([0])
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(p1.order))
    geneB = int(random.random() * len(p2.order))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene,endGene):
        childP1.append(p1.order[i])
    
    childP2 = [gene for gene in p2.order if gene not in childP1]

    child.order = childP1 + childP2

    return child

# data = init()
# population = populate(10,20)
# initpop = copy.deepcopy(population)
# combinaisons = (list(itertools.combinations(range(0,10),2)))
# distMatrix = compute_Dist_Matrix(data,combinaisons)

# bestOfGen = []
# for i in range(1000):
#     best = testPopulation(distMatrix,population)
#     normalizeFitness(population)
#     bestOfGen.append(best.length)
#     newPop = selection(population)
#     # print(list(path.order for path in newPop))
#     population = newPop[:]

# print(min(bestOfGen))


    
testpop = []

testpop.append(path([1,2,3,4,5,6,7,8,9],0.5,15))
testpop.append(path([1,3,2,4,5,6,7,8,9],0.25,17))
testpop.append(path([1,2,3,5,4,6,7,8,9],0.25,19))

child1 = breeding(testpop[0],testpop[1])
print(child1.order)
# picked = []
# for i in range(100):
#     picked.append(mutate(pickOne(testpop),0.5))

# pickedL = list(indiv.length for indiv in picked)

# print(pickedL.count(15))

# print(list(p.order for p in picked))