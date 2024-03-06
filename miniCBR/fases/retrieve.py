from miniCBR.cases.index import Indexacio
from miniCBR.cases.case import Cas
from typing import Tuple, List
from scipy.spatial.distance import euclidean

def find_leaf(indexacio: Indexacio, cas: Cas) -> Tuple[Cas, List]:
    node_actual = indexacio
    labels = []

    while not node_actual.leaf():
        kmeans = node_actual.get_root()
        label = kmeans.predict([cas.descripcio])[0]
        labels.append(label)
        
        if label == 0:
            node_actual = node_actual.get_left()
        else:
            node_actual = node_actual.get_right()

    return node_actual, labels # .get_root() si vols la llista de casos       

def most_similar(indexacio, new_case)-> List[Tuple[float, Cas, List[int]]]:
    """
    Find the most similar cases to a new case, and return them along with the distance 
    to the new_case and the path taken to find them.
    """
    n = indexacio.casesxleaf

    leaf, path = find_leaf(indexacio, new_case)
    originalpath = path.copy()
    cases = [(c, originalpath) for c in leaf.get_root()]
    
    distances = [[euclidean(new_case.descripcio, case.descripcio), case, path] for case, path in cases]
    distances.sort(key=lambda x: x[0])
    most_similar_case = distances[0]

    return most_similar_case