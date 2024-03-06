from typing import Any, Tuple, List
from CBR.cases.problem import Problem, scale_features
from numpy import ndarray
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist, squareform

class Cas:
    def __init__(
        self,
        id: str,
        descripcio: ndarray[Any], # El nostre problema ja preprocessat
        derivacio = set(),
        historial = [],
        solucio: List[int] = [],
        avaluacio: List[int] = [],
        cops_us: int = 0,
        
        utilitat: None = None,
        UM: int = 0,

        UaS: int = 0,
        S: int = 0,
        UaF: int = 0,
        F: int = 0,
        
    ) -> None:
        self.id = id
        self.descripcio = descripcio
        self.derivacio = derivacio
        self.solucio = solucio # llista de 3 llibres recomanats
        self.avaluacio = avaluacio # num del 1-5
        self.historial = historial

        #Calcul utilitat
        self.UM =UM # Utilitat normalitzada
        self.UaS = UaS #el nombre de vegades que es va utilitzar el cas i hi vahaver un èxit, quan el cas es trobava entre els casos recuperats
        self.S = S #quantitat total d'èxits quan el cas es trobava entre els casos recuperats
        self.UaF = UaF #número de vegades que s’ha utilitzat el cas i va ser un fracàs, quan el cas es trobava entre els casos recuperats
        self.F = F #número total de fracassos quan el cas es trobava entre els casos recuperats

        self.ultim = False
    
    def __repr__(self) -> str:
        return f"Cas(id={self.id}, descripcio={self.descripcio}, solucio={self.solucio}, avaluacio={self.avaluacio})"
    
    def actualitzar_Utilitat_normalitzada(self):
        s_div = 0 if self.S==0 else self.UaS/self.S
        f_div = 0 if self.F==0 else  self.UaF/self.F
        self.UM = ((s_div)-(f_div)+1)/2
    

def createDB(df:pd.DataFrame) -> List[Cas]:
    '''
    Funció que donat un csv en format DataFrame de pandas retorna una llista de casos.
    '''
    problemes = []

    for cas in df[df.columns[2:-2]].values:
        problemes.append(Problem(*cas))

    read_books = [eval(i) for i in df['read_books'].tolist()]
    recomendations = [eval(i) for i in df['recomendations'].tolist()]
    rating_recom = [eval(i) for i in df['recom_ratings'].tolist()]

    scaler, scaled_features = scale_features(problemes)

    db = [Cas(id=df['user_id'][idx], descripcio=p, historial=read_books[idx] ,solucio= recomendations[idx], avaluacio= rating_recom[idx]) for idx,p in enumerate(scaled_features)]
    
    return db, scaler

def redundant_optim(similar_cases: List[Cas], indices_cases:List[int], T_common_books, T_common_recom, T_common_rating, T_distance):
    
    pairwise_distances = pdist([i.descripcio for i in similar_cases], metric='euclidean')
    distance_matrix = squareform(pairwise_distances)

    # print(distance_matrix)

    redundant_cases = set()

    for i, index in enumerate(indices_cases):
        for j in range(i + 1, distance_matrix.shape[0]):
            punt = 0
            common_read_books = len(set(similar_cases[i].historial) & set(similar_cases[j].historial))
            common_recom = len(set(similar_cases[i].solucio) & set(similar_cases[j].solucio))
            common_rating = (abs(np.mean(similar_cases[i].avaluacio) - np.mean(similar_cases[j].avaluacio))) 
            if common_read_books >= T_common_books:
                punt += 1
            if common_recom >= T_common_recom:
                punt += 1
            if common_rating <= T_common_rating:
                punt += 1
            if distance_matrix[i, j] < T_distance:
                punt += 1
            if punt >= 3: redundant_cases.add(index)
    return redundant_cases


def redundant_clustering(clustering_cases: List[Cas], parametres):
    """crea un clustering amb totes les dades inicials. Aquest clustering
        servirà per a eliminar aquells casos redundants"""
    numeric_data = [case.descripcio for case in clustering_cases]
    T_common_books, T_common_recom, T_common_rating, T_distance = parametres


    # Creem un arbre jerarquic a partir d'obserbar el dendograma
    final_model_adjusted = AgglomerativeClustering(n_clusters=None,  
                                                    distance_threshold= 2,
                                                    linkage='ward')
    final_model_adjusted.fit(numeric_data)

    #indica a quin cluster pertany cada cas. Llista de etiquetes
    clusters_adjusted = final_model_adjusted.labels_ 
    cluster_counts = np.unique(clusters_adjusted, return_counts=True)
    delete_indexes = []

    for cluster in range(len(cluster_counts[1])):
        cluster_indices = np.where(clusters_adjusted == cluster)[0]
        cluster_data = [clustering_cases[idx] for idx in cluster_indices]
        delete_index = redundant_optim(cluster_data, cluster_indices, T_common_books, T_common_recom, T_common_rating, T_distance)
        delete_indexes += delete_index
    

    #print('Abans de la eliminació de redundants hi ha', len(clustering_cases), 'casos')
    new_cases = []
    for idx, case in enumerate(clustering_cases):
        if idx not in delete_indexes:
            new_cases.append(case)

    #print('Després de la eliminació de redundants hi ha', len(new_cases), 'casos')
    return new_cases

