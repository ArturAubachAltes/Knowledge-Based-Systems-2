from miniCBR.fases import *
from miniCBR.cases import *
import random

class RecommenderSystem:
    def __init__(
            self, 
            maxcasesxleaf:int = 5,
            casebase:pd.DataFrame=None
        ) -> None:
        db, self.scaler = createDB(casebase)
        self.casebase = db 
        self.indexacio = Indexacio(casesbase=self.casebase, casesxleaf=maxcasesxleaf)

    def retrieve(self, newcase:Cas) -> Tuple[float, Cas, List[int]]:
        return most_similar(self.indexacio, newcase)
    
    def reuse(self, case, newcas) -> bool:
        '''
        True if we use the returned case from retrieve. Else False

        In this minimal form we don't do any adaptation.
        '''
        newcas.solucio = case.solucio.copy()

    def revise(self, newcas):
        '''
        Assigna un valor enter aleatori com a recomanació. No dona 
        l'opció a no llegir el llibre.
        '''
        newcas.avaluacio = [random.randint(1,5) for _ in range(3)]
        return newcas.avaluacio 

    def retain(self, dist, newcas, path, T=0.9):
        '''
        Acull el nou cas si la distància es superior al threshold T.

        Sols mira redundància com a criteri. No té en compte l'avaluació
        de l'usuari.
        '''
        if dist > T:
            self.indexacio.add(newcas, ruta=path)
            print('Adding the new case.')
        else:
            print('New case is redundant')

def createRS(casebase:pd.DataFrame, maxcasesxleaf:int = 10):
    rs = RecommenderSystem(maxcasesxleaf=maxcasesxleaf,casebase=casebase)
    return rs
