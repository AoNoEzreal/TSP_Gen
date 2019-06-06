# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:13:51 2019

@author: ybett
"""
import csv
import math
import itertools
import time



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = x

def distance(x1,y1,x2,y2):
    #print('x1 = ',x1,' y1 = ', y1,' x2 = ', x2, ' y2 = ',y2)
    d = abs(math.sqrt(((x1-x2)**2) + ((y1-y2)**2)))
    return d

def distPath(path,data):
    tot = 0
    for i in (range(len(path)-1)):
        index = path[i]
        nextIndex = path[i+1]
        d = distance(data[index][0],data[index][1],data[nextIndex][0],data[nextIndex][1])
        tot = tot + d
    last = path[-1]
    retour = distance(data[last][0],data[last][1],data[0][0],data[0][1])

    return tot + retour  # On ajoute le retour au point de départ

def init():
    results = []
    nb =0
   
    with open('data/test10.csv','r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if(nb == 0):
                nb = int(row[0]) # On convertit le premier element en entier
            else :
                results.append(row)

        for i in range(0,len(results)):
            for j in range(0,len(results[i])):
                results[i][j] = float(results[i][j])
    return results

def calc(perms,results,nb):
    res = []
    for i in range(Length):
        res.append(distPath(permutations[i],results))   
        

def compute_Dist_Matrix(data,combi):
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

def calc_path(dists,path):
    #print (path)
    first = path[0]
    tot = 0
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        #print(dists[p1,p2])
        tot = tot + dists[p1,p2]

    return tot + dists[p2,0] + dists[0,first]

start = time.time()
res = []
data = init()
nb = len(data)
fact = math.factorial(nb - 1)
permutations = list(itertools.permutations(range(1,nb)))


#permutations = permutations[:fact]
Length = len(permutations)/2
permutations = permutations[:Length]
combinaisons = (list(itertools.combinations(range(0,nb),2)))
Dist_Matrix = compute_Dist_Matrix(data,combinaisons)  # Table contenant toutes les distances 
# calc(permutations,data,len(data))


for i in range(Length):
    res.append(calc_path(Dist_Matrix,permutations[i]))



print(min(res))
end = time.time()
print(end-start)
 
