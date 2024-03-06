"""
Funció: Adapta les solucions dels casos recuperats a la nova situació.

Components: Algoritmes per ajustar les recomanacions basades en els casos recuperats.
"""
from operator import add
from collections import defaultdict
from CBR.cases.index import Indexacio
from CBR.cases.case import Cas
from typing import Tuple, List
from scipy.spatial.distance import euclidean

def confianza(casos_similars: List[Tuple[float, Cas]], new_case: Cas) -> dict[str:List[int]]:
    """

    A partir d'una llista de casos similars i un nou cas, retorna un diccionari amb la informació dels 3 llibres a recomanar
    -> {id_llibre: [valoracions_predita,[casos_similar_que_contenen_el_llibre]]}

    """
    # confxlibro = {}  # {id llibre: [valor, dis,[casos]]}

    confxlibro = defaultdict(lambda: [0, 0, []])

    for distancia, caso in casos_similars:
        
        similitud = 1 / (distancia+1) 

        for idx, libro in enumerate(caso.solucio):
            if (aval := caso.avaluacio[idx]) != 0:
                # Calculado una sola vez
                valor = aval * similitud
                confxlibro[libro][0] += valor
                confxlibro[libro][1] += similitud
                confxlibro[libro][2].append(caso)
    
    sortedconf = sorted(
        ((id_llibre, [ valor / simil, cases])
         for id_llibre, (valor, simil, cases) in confxlibro.items()),
        key=lambda item: item[1][0], reverse=True
    )

    tres_primers = dict(sortedconf[:3])
    for _, casos in tres_primers.values():
        for cas in casos:
            new_case.derivacio.add(cas.id)
    new_case.solucio = list(tres_primers.keys())

    if len(new_case.solucio) < 3:
        print(tres_primers)
        print(sortedconf)
        print(casos_similars)

    return tres_primers
