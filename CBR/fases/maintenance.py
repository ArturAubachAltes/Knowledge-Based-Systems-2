"""
Funció: Incorpora la nova experiència (cas d'ús actual) a la base de dades per a futurs usos.

Components: Mecanismes per a l'actualització de la base de dades amb nous casos.
"""
from CBR.cases import Cas, Indexacio, Problem
from CBR.fases import most_similar
import random
import timeit
from datetime import timedelta
from time import time

def generate_new_problem():
    # Generar una llista de l'1 al 10 representant l'ordre de preferència dels gèneres
    genres = random.sample(range(1, 11), 10)
 
    # Generar el nombre mitjà de pàgines que llegeix el lector: int en el rang de 100 a 400
    avg_pages = random.randint(100, 400)
    
    # Generar el contatge de llibres llegits pel lector: int en el rang de 1 a 200
    count_read = random.randint(1, 200)
    
    # Generar la puntuació mitjana que dona el lector als llibres: float en el rang de 1 a 5
    avg_rating = random.uniform(1, 5)
    
    # Crear el new_case com una cadena

    newp = ','.join(map(str, genres + [avg_pages, count_read, avg_rating]))
    newp = 'Problem(' + newp + ')'
    
    return newp

def calcular_temps(rs):
    num_cases = 2000  # Número de casos de prueba a generar
    execution_times = []

    for _ in range(num_cases):
        newp_str = generate_new_problem()
        newp = eval(newp_str)
        newcas = Cas(id=(rs.indexacio.ultim_id),descripcio=rs.scaler.transform([newp.array])[0])
        # Medir el tiempo de ejecución de most_similar para este new_case
        time_taken = timeit.timeit(lambda: most_similar(rs.indexacio, newcas), number=1)
        execution_times.append(time_taken)

    media_tiempo = sum(execution_times) / len(execution_times)
    print('La mitjana del temps es:',media_tiempo)
    return media_tiempo


init_time = time()
#print(f"Total Running time {timedelta(seconds=(time() - init_time))}")