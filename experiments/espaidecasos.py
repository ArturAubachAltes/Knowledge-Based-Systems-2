from CBR import *
import numpy as np
import random
import pandas as pd
import time
import matplotlib.pyplot as plt

def block(rs:RecommenderSystem, blocksize:int=100):
    
    redundants = 0
    for _ in range(blocksize):
        newp = eval(generate_new_problem())    
        
        most_similar_cases, newcas = rs.retrieve(newp)
        distancies, casos, paths = zip(*most_similar_cases)
        cas_dists = list(zip(distancies, casos))
        dicc_most_sim = rs.reuse(cas_dists, newcas)
        rs.revise(newcas, casos, dicc_most_sim, False) 
        redundancia = rs.retain(newcas, cas_dists, paths[0], 2)
        if redundancia == 1:
            redundants += 1

    return redundants/blocksize

df_problemes = pd.read_csv('./data/problems4000_not_0_0_0.csv')
rs = createRS(
    from_model= False, 
    casebase=df_problemes, 
    maxcasesxleaf=15
)

num_blocks = 100
rates = []

for b in range(num_blocks):
    rate = block(rs)
    rates.append(rate)
    print(f'Rati en el block {b} = {rate}')

plt.plot(range(num_blocks), rates, marker='o')  # 'o' adds dots at each point
plt.xlabel('Quantitat de Blocs Afegits')
plt.ylabel('Rati de Casos Redundants per bloc')
plt.title('Evolució del Rati de Casos Redundants') 
plt.savefig('./images/espaidecasos1')
plt.show()
plt.close() 