import sys
from math import exp
import pandas as pd

import os

# s'execute directement avec la commande "Python get_features.py"

familys = [family for family in os.listdir('./data/') if len(family.split('.')) > 1 and family.split('.')[1] == 'txt' ]
familys = [family.split('_')[0] for family in familys]

familys_features = {family:[] for family in familys}

range_k = [4,20]

def get_nodes(feature,nodes_lines):
    nodes = list(range(1,len(feature)+1))
    proba = 1
    for i,char in zip(nodes,feature):
        proba *= nodes_lines[i][char] 
    for j in range(2, LENG + 1 - len(feature)):
        nodes_prime = list(range(j,len(feature)+j))
        proba_prime = 1
        for i,char in zip(nodes_prime,feature):
            proba_prime *= nodes_lines[i][char] 
        if proba_prime > proba:
            proba = proba_prime
            nodes = nodes_prime

    return nodes, proba

for family in familys:
    file = open('./data/'+family+"_alignments.txt",'r')
    hmm_file = open('./data/'+family+".hmm",'r')

    nodes_lines = {}

    line = next(hmm_file).replace('\n','').strip()
    while line[0:4] != 'LENG':
        line = next(hmm_file).replace('\n','').strip()
    LENG = int(line.split()[1])
    while line[0:5] != 'COMPO':
        line = next(hmm_file).replace('\n','').strip()
    # for i in range(2):
    next(hmm_file)
    # next(hmm_file)

    j = 1
    while j <= LENG:
        transitions = next(hmm_file).replace('\n','').strip()
        match_proba = exp(-float(transitions.split()[0]))
        line = next(hmm_file).replace('\n','').strip()
        assert int(line[0:len(str(LENG))]) == j , ' j is {} while line[0:2] is {}'.format(j,int(line[0:2]))
        nodes_lines[j] = [exp(-float(val))*match_proba for val in line.split()[1:5]]
        next(hmm_file)
        # next(hmm_file)
        j+=1

    for j in range(1,LENG+1):
        nodes_lines[j] = {"A" : nodes_lines[j][0], "C" : nodes_lines[j][1], "G" : nodes_lines[j][2], "U" : nodes_lines[j][3]}
    lines = [line.replace('\n','').upper() for line in file]
    lines = lines[:700]
    features = {}
    for k in range(range_k[0],range_k[1]+1):
        for line in lines:
            for i in range(len(line)):
                feature = line[i:i+k].replace('-','')
                if len(feature) < k or  feature in features.keys() or '-' in feature:
                    continue
                features[feature] = 0
                for line_2 in lines:
                    if feature == line_2[i:i+k]: 
                        features[feature] +=1
    for key in features.keys():
        nodes,proba = get_nodes(key,nodes_lines)
        features[key] = [features[key], nodes , proba]

    features = {a:b for a,b in sorted(features.items(), key=lambda x: (x[1][2],x[1][0]) ,reverse = True)}
    
    for i,v in enumerate(features.items()):
        if i == 10 :
            break
        familys_features[family].append(v[0])

for k,v in familys_features.items():
    print(k,'\t',v)