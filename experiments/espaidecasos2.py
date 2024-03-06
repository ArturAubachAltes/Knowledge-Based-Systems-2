from CBR import *
import numpy as np
import random
import pandas as pd
import time
import matplotlib.pyplot as plt

def block(rs:RecommenderSystem, blocksize:int=100):
    
    afegits = 0
    redundants = 0
    swaps = 0
    rating_user = 0
    rating_pred = 0

    for _ in range(blocksize):
        newp = eval(generate_new_problem())    
        
        most_similar_cases, newcas = rs.retrieve(newp)
        distancies, casos, paths = zip(*most_similar_cases)
        cas_dists = list(zip(distancies, casos))
        dicc_most_sim = rs.reuse(cas_dists, newcas)
        rs.revise(newcas, casos, dicc_most_sim, False) 
        redundancia = rs.retain(newcas, cas_dists, paths[0], 2)
        if redundancia == 0:
            afegits += 1
        elif redundancia == 1:
            redundants += 1
        elif redundancia == 2:
            swaps += 1
        rating_user += sum(newcas.avaluacio)
        rating_pred += sum([v[0] for v in dicc_most_sim.values()])

    avaluacio_mitjana = mean([r for c in rs.indexacio.casesbase for r in c.avaluacio])

    return round(afegits/blocksize,3), round(redundants/blocksize,3), round(swaps/blocksize,3), round(rating_user/(blocksize*3),3), round(rating_pred/(blocksize*3),3), round(avaluacio_mitjana,3)

df_problemes = pd.read_csv('./data/problems4000_not_0_0_0.csv')
rs = createRS(
    from_model= False, 
    casebase=df_problemes, 
    maxcasesxleaf=15
)

num_blocks = 200

afegits, redundants, swaps, ratings_u, ratings_p, av = [], [], [], [], [], []

for b in range(num_blocks):
    print(f'--- BLOC {b+1} ---')
    a, re, s, ra, rp, ava = block(rs)
    afegits.append(a)
    redundants.append(re)
    swaps.append(s)
    ratings_u.append(ra)
    ratings_p.append(rp)
    av.append(ava)
    print(f'Rati Afegits = {a}')
    print(f'Rati Redundants = {re}')
    print(f'Rati Swaps = {s}')
    print(f'Mitjana d\'Avaluacions de l\'Usuari = {ra}')
    print(f'Mitjana d\'Avaluacions Predites = {rp}')
    print(f'Mitjana d\'Avaluacions dels Casos = {ava}')
    print()

plt.figure(figsize=(12, 6))
plt.plot(range(num_blocks), afegits, label='Afegits')
plt.plot(range(num_blocks), redundants, label='Redundants')
plt.plot(range(num_blocks), swaps, label='Swaps')
plt.xlabel('Quantitat de Blocs Afegits')
plt.ylabel('Valor del Rati per bloc')
plt.title('Evolució dels Ratis de Redundància') 
plt.legend()
plt.savefig('./images/espaidecasos4')
plt.show()
plt.close() 

plt.figure(figsize=(12, 6))  # Ancho de 12 pulgadas y altura de 6 pulgadas
plt.plot(range(num_blocks), ratings_u, label='User Ratings')
plt.plot(range(num_blocks), ratings_p, label='Pred Ratings')
plt.plot(range(num_blocks), av, label='Mean Ratings')
plt.xlabel('Quantitat de Blocs Afegits')
plt.ylabel('Rating Mitjà per Bloc')
plt.title('Evolució dels Ratings') 
plt.legend()
plt.savefig('./images/espaidecasos5')
plt.show()
plt.close()
