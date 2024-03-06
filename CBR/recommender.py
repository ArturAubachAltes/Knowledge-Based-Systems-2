from CBR.fases import *
from CBR.cases import *
from typing import Set
import pickle

class RecommenderSystem:
    def __init__(
            self, 
            maxcasesxleaf:int = 5,
            casebase:pd.DataFrame=None,
            
            #Experimentacio redundant
            parametres: List = [],
            # Calcular Eval
            n_correct: int = 0, #numero de prediccions correctes
            n_predictons: int = 0, #numero de casos evaluats

            #Calcualr com de real es la prediccio
            AE:int = 0, # Sumatorio de las diferencias absolutas entre las puntuaciones predichas y las reales para todos los libros y todos los usuarios
            num_casos_valorats: int=0, # Numero de casos valorats

            r_min = 1,
            r_max = 5,

            cas_nr = 0,
            cas_r_u = 0

        ) -> None:
        '''
        r_max -> maxim d'estrelles a la valoració
        r_min -> minim d'estrelles a la valoració
        '''

        db, self.scaler = createDB(casebase)
        self.casebase = redundant_clustering(db, parametres)
        self.indexacio = Indexacio(casesbase=db, casesxleaf=maxcasesxleaf)
        
        # Eval
        self.n_correct  = n_correct
        self.n_predictons =  n_predictons
        
        self.r_max = r_max
        self.r_min = r_min
             
        self.AE = AE
        self.num_casos_valorats = num_casos_valorats

        self.cas_nr = cas_nr
        self.cas_r_u = cas_r_u

    def save(self, nombre_archivo_sin_extension):
        nombre_archivo_completo = f"{nombre_archivo_sin_extension}.pkl"
        with open(nombre_archivo_completo, 'wb') as archivo:
            pickle.dump(self, archivo)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as archivo:
            instancia = pickle.load(archivo)
        return instancia

    def retrieve(self, newp:Problem) -> Tuple[List[Tuple[float, Cas, List[int]]],Cas]:
        newcase = Cas(id=self.indexacio.ultim_id,descripcio=self.scaler.transform([newp.array])[0])
        return most_similar(self.indexacio, newcase), newcase
    
    def reuse(self, casos_sim, newc):
        result = confianza(casos_sim, newc)
        return result

    def revise(self, cas, casos, diccion, user_eval:bool = False,evaluation=[]):
        if user_eval:
            user_evaluation(cas, self,evaluation)  # Forma manual
        else:
            predict_evaluation(cas, self) # Usant predictiu
        recompte_valors_utilitzats(cas, casos, diccion)
        calcAE(cas,diccion,self)

    def retain(self, cas, cas_dist:List[Tuple[float, Cas]], list_path:List[int], T: int = 1):
        
        redundancia = redundant_cas(cas, cas_dist, T)
        if redundancia == 0:
            # print("Cas no redundant i s'ha indexat")
            self.indexacio.add(cas,list_path)
            self.cas_nr += 1
            return 0
        elif redundancia == 1:
            # print("Cas redundant")
            return 1
        elif redundancia == 2:
            # print("Cas redundant i ÚTIL")
            self.cas_r_u += 1
            return 2

    def maintenance(self, T = 0.002, E = 350000):
        '''
        T -> timesteps
        E -> spacesteps
        '''
        if calcular_temps(self) >= T or self.indexacio.space >= E:
            self.indexacio.refer_base()
            self.cas_r_u = 0
            self.cas_nr = 0

    @property
    def evaluation(self):
        return (self.n_correct/self.n_predictons)*2 if self.n_predictons != 0 else 0

    @property
    def NMAE(self):
        return (self.AE/self.num_casos_valorats)/(self.r_max - self.r_min)


def createRS(from_model:bool, path:str = None, maxcasesxleaf:int = 44, params:List = [5, 2, 0.5, 0.1], casebase:pd.DataFrame = None):
    if from_model:
        rs = RecommenderSystem.load(path)
    else:
        try:
            casebase.drop('Unnamed: 0',axis=1,inplace=True)
        except:
            pass
        rs = RecommenderSystem(maxcasesxleaf=maxcasesxleaf,casebase=casebase, parametres= params)
    return rs

