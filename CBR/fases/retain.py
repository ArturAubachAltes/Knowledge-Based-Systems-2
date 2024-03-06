from CBR.cases.index import Indexacio
from CBR.cases.case import Cas
from typing import Tuple, List
from scipy.spatial.distance import euclidean
from statistics import mean

# Retain
def redundant_cas(new:Cas, most_similars:List[Tuple[float, Cas]], T:int = 1, learn:bool = True):
    '''
    Retorna:
        0 si NO és redundant
        1 si SÍ és redundant
        2 si SÍ és redundant però MILLOR (Swap)
    '''
    if len(new.solucio) == 1:
        print('most_similars', most_similars)
    if len(new.solucio) < 3 or len(new.avaluacio) < 3:
        print(new.__dict__)
    
    dicc = {new.solucio[i]: new.avaluacio[i] for i in range(3)}
    dicc_keys_set = set(dicc.keys())  # Convertir las claves en un conjunto
    for dist, case in most_similars:
        if dist < T:
            coincident_books = 0
            for book in dicc_keys_set.intersection(case.solucio):
                if abs(dicc[book] - case.avaluacio[case.solucio.index(book)]) <= 1.5:
                    coincident_books += 1
                    if coincident_books >= 2:
                        
                        # APRENENTATGE

                        #Tipus Normal
                        # if learn and better(old=case, new=new):
                        #     swap(old=case,new=new)
                        #     return 2

                        # Tipus Greedy
                        oldsol = case.solucio.copy()
                        greedyswap(old=case, new=new)
                        if oldsol != case.solucio:
                            return 2

                        return 1
        else:
            return 0
    return 0

def better(old:Cas, new:Cas):
    return mean(new.solucio) > mean(old.solucio)

def swap(old:Cas, new:Cas):
    old.__dict__, new.__dict__ = new.__dict__.copy(), old.__dict__.copy()

def greedyswap(old:Cas, new:Cas):

    na, ns, oa, os = new.avaluacio.copy(), new.solucio.copy(), old.avaluacio.copy(), old.solucio.copy()

    l = []
    for idx in range(3):
        l.extend([(na[idx], ns[idx]), (oa[idx], os[idx])])
    l.sort(key=lambda x:x[0],reverse=True)
    
    avaluacio, solucio = [], []
    for a,s in l:
        if len(solucio) == 3:
            break
        if s not in solucio:
            avaluacio.append(a)
            solucio.append(s)


    if len(list(avaluacio).copy()) < 3 or len(list(solucio).copy()) < 3:
        print('PROBLEMA')
        print(l)
        print(avaluacio)
        print(solucio)
    
    old.avaluacio = list(avaluacio).copy()
    old.solucio = list(solucio).copy()
