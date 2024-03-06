from typing import Any, Tuple, List
from miniCBR.cases.problem import Problem, scale_features
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
        derivacio = None,
        historial = [],
        solucio: List[int] = [],
        avaluacio: List[int] = []
        
    ) -> None:
        self.id = id
        self.descripcio = descripcio
        self.derivacio = derivacio
        self.solucio = solucio # llista de 3 llibres recomanats
        self.avaluacio = avaluacio # num del 1-5
        self.historial = historial
    
    def __repr__(self) -> str:
        return f"Cas(id={self.id}, solucio={self.solucio}, avaluacio={self.avaluacio})"

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
