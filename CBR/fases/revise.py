"""
Funció: Revisa i modifica les recomanacions proposades abans de presentar-les a l'usuari.

Components: Funcions per a la validació i ajust de recomanacions.
"""

from CBR.cases.index import Indexacio
from CBR.cases.case import Cas
from typing import Tuple, List
from scipy.spatial.distance import euclidean
import pandas as pd
import pickle
import xgboost as xgb
import numpy as np

# Funció per convertir un Cas a una representació vàlida per a obtenir la predicció del model xgboost
def convert_case_to_data(newcas:Cas):
    '''
    Roar roar
    '''
    non_important = ['Fantasy_x', 'Poetry_x']
    newcas = [newcas]
    problems = [list(cas.descripcio) + [str(cas.solucio)] for i, cas in enumerate(newcas)]
    # Definir las columnas del DataFrame
    column_names = ['Fantasy', 'Fiction', 'Mystery', 'Poetry',
                    'History', 'Romance', 'Non-fiction', 'Children', 'Young-adult',
                    'Comics', 'mean_length', 'count_reads', 'avg_rating','books_ids']

    # Crear el DataFrame
    df = pd.DataFrame(problems, columns=column_names)
    df['books_ids'] = df['books_ids'].apply(eval)
    # Utilizar explode para expandir los elementos de la lista en filas separadas
    df_exploded = df.explode('books_ids')
    # Cambiar el nombre de la columna 'lista' a 'nuevo_nombre'
    df_exploded = df_exploded.rename(columns={'books_ids': 'book_id'})
    
    bk_merge = pd.read_csv('data/genres_pages_x_books.csv')
    bk_merge.drop('Unnamed: 0',axis=1,inplace=True)
    final_dataset = df_exploded.merge(bk_merge, on='book_id', how='inner')
    final_dataset.drop(non_important,axis=1,inplace=True)
    final_dataset.drop(['book_id'],axis=1,inplace=True)
    return final_dataset

def predict_evaluation(newcas:Cas,rs): # Se pot canviar el paràmetre per un path fixe si decidim quedarnos amb un model
    with open('xgb_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    dataset = convert_case_to_data(newcas)
    estimacio = np.clip(np.round(np.array(loaded_model.predict(dataset))), 0, 5).astype(int).tolist()
    newcas.avaluacio = estimacio
    for val in estimacio:
        rs.n_correct += val
        rs.n_predictons += 1    

def valorate(new_case:Cas, idx:int, rs):
    '''
    Si val == 0, semanticament indica que no ha comprat el llibre recomanat
    '''
    val = float('-inf')
    while val not in list(range(6)):
        val = int(input(f"Què t'ha semblat el llibre {new_case.solucio[idx]}, quantes estrelles li dones? (1-5): "))
        rs.n_correct += val
        rs.n_predictons += 1

    return val

def user_evaluation(newcas:Cas, rs, evaluation):
    newcas.avaluacio = evaluation

# Calcul Utilitat Normalitzada
def recompte_valors_utilitzats(newcas:Cas, llista_casos_similars:List[Cas], dic_casos_utilitzats):
    '''
    newcas -> Cas:
        Cas nou introduït.
    
    llista_casos_similars -> List[Cas]:
        Llista ordenada dels casos més similars. Extreta de most_similiar() del retrieve
    
    dic_casos_utilitzats -> dict[str:List[int|Cas]]:
        {id_llibre: [valoracions_predita,[casos_similar_que_contenen_el_llibre]]}
    '''
    pos, neg = 0, 0
    for i, key in enumerate(dic_casos_utilitzats.keys()):
        if newcas.avaluacio[i] > 3.5:
            pos += 1
            for cas_pos in dic_casos_utilitzats[key][1]:
                cas_pos.UaS += 1

        else:
            neg += 1
            for cas_neg in dic_casos_utilitzats[key][1]:
                cas_neg.UaF += 1

    for cas in llista_casos_similars:
        cas.S += pos
        cas.F += neg

        cas.actualitzar_Utilitat_normalitzada()

# Calcul Error Absoluto Medio Normalizado
def calcAE(newcas: Cas, dic_casos_utilitzats,rs):
    """"
    new:

    dic_casos_utilitzats:
    """
    
    num_punt = 0
    for index, llibre in enumerate(newcas.solucio):
        if newcas.avaluacio[index] is not None and dic_casos_utilitzats[llibre][0] is not None:
            num_punt += abs(newcas.avaluacio[index] - dic_casos_utilitzats[llibre][0])
            rs.num_casos_valorats += 1

    if num_punt > 0:
        rs.AE += num_punt