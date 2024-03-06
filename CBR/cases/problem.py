from typing import List
from sklearn.preprocessing import MinMaxScaler
from collections import namedtuple
import numpy as np

from CBR.constants import *

class Problem:
    '''
    Classe Abstracta de Lector i altres components del problema:
    - fantasy : de tots els llibres que ha llegit, el percentatge que són de fantasia
    - fiction : de tots els llibres que ha llegit, el percentatge que són de ficció
    - mystery : de tots els llibres que ha llegit, el percentatge que són de misteri
    - poetry : de tots els llibres que ha llegit, el percentatge que són de poesia
    - history : de tots els llibres que ha llegit, el percentatge que són de historia
    - romance : de tots els llibres que ha llegit, el percentatge que són romantics
    - nonfiction : de tots els llibres que ha llegit, el percentatge que no son de ficcio
    - children : de tots els llibres que ha llegit, el percentatge que són de nens
    - youngadult : de tots els llibres que ha llegit, el percentatge que són de adolescents
    - comics : de tots els llibres que ha llegit, el percentatge que són de comics
    - (TODO) major_cover : format de llibre preferit
    - mean_length : mitjana de la longitud de tots els llibres que ha llibre
    - num_reads : quantitat de llibres llegits
    - (TODO: com d'exigent ets?) avg_rating : mitjana de la puntuació que ha posat als llibres llegits


    '''
    def __init__(
        self,
        fantasy:float, fiction:float, mystery:float, poetry: float, history: float, romance: float,
        nonfiction: float, children: float, youngadult: float, comics: float, 
        mean_length: float, count_reads: int, avg_rating: float) -> None:
        
        self.fantasy = fantasy
        self.fiction = fiction
        self.mystery = mystery
        self.poetry = poetry
        self.history = history
        self.romance = romance 
        self.nonfiction = nonfiction
        self.children = children
        self.youngadult = youngadult
        self.comics = comics
        self.mean_length = mean_length
        self.count_reads = count_reads
        self.avg_rating =  avg_rating

        self.array = list(self.__dict__.values())

    def __repr__(self):
        return f"Problem()"

def scale_features(problems: List["Problem"]) -> np.ndarray:
    '''
    Function to scale features between 0 and 1
    '''
    features = np.array([problem.array for problem in problems])

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(features)

    for s, p in zip(scaled_features, problems):
        p.array = list(s)

    return scaler, scaled_features
