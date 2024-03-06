import numpy as np
from .bintreelinked import BinTree
from typing import List, Any, Tuple
from .case import Cas
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.spatial.distance import euclidean
import sys

class Indexacio(BinTree):
    def __init__(
        self, 
        casesbase=None, 
        left=None, right=None, 
        type:str='', 
        casesxleaf:int = 10,

    ) -> None: # type - str, per a determinar quin tipus de creacio s'executa.

        super().__init__(casesbase, left, right)
        
        self.ultim_id = len(casesbase)
        self.type = type
        self.casesxleaf = casesxleaf

        self.creacio(casos=casesbase)
        self.ultims_casos = []
        self.casesbase = casesbase

    def __len__(self):
        return self.__length

    def creacio(self,casos:List[Cas]) -> None:
        self.__length = len(casos)
        if len(casos) <= self.casesxleaf:
            # Si només hi ha un cas, retorna un arbre amb aquest cas.
            self.set_root(casos)
        else:
            # Aplicar KMeans per a dividir els casos en grups.
            kmeans = KMeans(n_clusters=2, random_state=0, n_init='auto')
            kmeans.fit([cas.descripcio for cas in casos])

            # Dividir els casos segons les etiquetes del clustering.
            cluster1 = [casos[i] for i in range(len(casos)) if kmeans.labels_[i] == 0]
            cluster2 = [casos[i] for i in range(len(casos)) if kmeans.labels_[i] == 1]

            # Crear els subarbres per a cada cluster.
            subarbre1 = Indexacio(casesbase=cluster1, casesxleaf=self.casesxleaf) 
            subarbre2 = Indexacio(casesbase=cluster2, casesxleaf=self.casesxleaf)

            # Retorna un arbre amb l'objecte KMeans com a arrel i els subarbres com a fills.
            self.set_root(kmeans)
            self.set_left(subarbre1)
            self.set_right(subarbre2)

    # ========================================================================
    def add(self, new:Cas, ruta:List[Any]):
        """
        Afegeix un nou cas a l'arbre utilitzant la ruta del cas més similar.
        """
        self.casesbase.append(new)

        # Recórrer l'arbre fins al node més similar.
        new.ultim = True
        if len(self.ultims_casos) == 50:
            self.ultims_casos[0].ultim = False
            self.ultims_casos = self.ultims_casos[1:] + [new]
        else:
            self.ultims_casos = self.ultims_casos + [new]

        self.__length += 1
        self.ultim_id += 1
        node_actual = self
        for label in ruta:
            if label == 0:
                node_actual = node_actual.get_left()
            else:
                node_actual = node_actual.get_right()

        # Obtenir el cas del node més similar i afegir el nou cas.
        leafcases = node_actual.get_root() + [new]
        #self.casesbase.append(new)

        if len(leafcases) >= self.casesxleaf:
            # Crear un nou KMeans amb tots els casos.
            kmeans = KMeans(n_clusters=2, random_state=0, n_init='auto')
            kmeans.fit([cas.descripcio for cas in leafcases])
            
            # Dividir els casos segons les etiquetes del clustering.
            for idx, i in enumerate(kmeans.labels_):
                if i == 0:
                    cluster1 = [leafcases[idx]]
                else:
                    cluster2 = [leafcases[idx]]
            
            # Crear els nous subarbres.
            subarbre1 = Indexacio(casesbase=cluster1, casesxleaf=self.casesxleaf) 
            subarbre2 = Indexacio(casesbase=cluster2, casesxleaf=self.casesxleaf)

            # Actualitzar el node actual amb el nou cluster i subarbres.
            node_actual.set_root(kmeans)
            node_actual.set_left(subarbre1)
            node_actual.set_right(subarbre2)
        
        else:
            node_actual.set_root(leafcases)

    '''
    MANTENIMENT DE LA BASE DE CASOS
    '''

    def llista_casos(self,llindar_utilitat=0): 
        """Retorna la llista de casos. 
            En cas de definir el llindar de utilitat serveix per trobar 
            els casos amb una utilitat superior a aquesta
        """
        def dfs(node):
            if node.empty():
                return []

            if node.leaf():
                return [cas for cas in node.get_root() if (cas.UM >= llindar_utilitat) or cas.ultim]
            
            return dfs(node.get_left()) + dfs(node.get_right())
        return dfs(self)

    def find_casos_utils(self):
        llindar_utilitat = 0
        return self.llista_casos(llindar_utilitat)

    def refer_base(self):
        llista_casos_utils = self.find_casos_utils()
        self.creacio(llista_casos_utils)

    @property
    def space(self):
        def calculate_space(node):
            if node is None or node.empty():
                return 0

            size = sys.getsizeof(node)
            size += calculate_space(node.get_left())
            size += calculate_space(node.get_right())

            if node.leaf():
                for cas in node.get_root():
                    size += sys.getsizeof(cas)

            return size

        return calculate_space(self)