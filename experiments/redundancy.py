from CBR import *
import pandas as pd
import matplotlib.pyplot as plt
from time import time

def exp_retain(threshold):
    print('ja')
    num_cases = 20
    df_problemes = pd.read_csv('./data/problems4000_not_0_0_0.csv')
    rs = createRS(from_model= False, casebase=df_problemes)

    avaluacio, qualitat = [], []
    redundants = 0

    for _ in range(num_cases):
        newp_str = generate_new_problem()
        newp = eval(newp_str)  
        
        most_similar_cases, newcas = rs.retrieve(newp) # Retrieve

        distancies, casos, paths = zip(*most_similar_cases) # Reuse
        cas_dists = list(zip(distancies, casos))
        dicc_most_sim = rs.reuse(cas_dists, newcas)

        rs.revise(newcas, casos, dicc_most_sim, False) # Revise

        r = rs.retain(newcas, cas_dists, paths[0], threshold) # Retain
        redundants += 1 if r==1 else 0

        avaluacio.append(rs.evaluation)
        qualitat.append(rs.NMAE)

    redundancy_rate = redundants/num_cases
    return avaluacio, qualitat, redundancy_rate


def plot_data(data, title, file, cases, xlabel, ylabel):
    for i, sublist in enumerate(data):
        plt.plot(sublist, label=f'{cases[i]} distance threshold')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt. xticks(rotation=90)
    # Situar la leyenda fuera del área de trazado, a la izquierda y con un tamaño de letra más pequeño.
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')

    plt.savefig(f'./images/{file}')
    plt.show()
    plt.close()


distance_thresholds = [0]+[round(i*0.5,1) for i in range(1,11)]
avaluacions, nmaes, rrate = [], [], []

for threshold in distance_thresholds:
    aval, qual, r = exp_retain(threshold)
    avaluacions.append(aval)
    nmaes.append(qual)
    rrate.append(r)

plot_data(avaluacions, 'Avaluacions per a diferents valors de Thresholds', 'redundancy_aval', distance_thresholds, 'Nous casos afegits' , 'Qualitat de la avaluació')
plot_data(nmaes, 'Resultats de NMAE per a diferents valors de Thresholds', 'redundancy_nmaes', distance_thresholds, 'Nous casos afegits', 'Quantitat de Mnae')


rates = rrate
# Etiquetas para las barras (opcional)

# Crear el gráfico de barras
plt.bar(range(len(rates)), rates, tick_label=[str(l) for l in distance_thresholds])
plt.xlabel('Percentatge de casos redundants')
plt.ylabel('Num de nous casos afegits')
plt. xticks(rotation=90)
plt.title('Gráfic de Barras per estudiar la distància de redundancia' )

# Mostrar el gráfico
plt.savefig('./images/redundancy_rate')
plt.show()
plt.close()

#############################
#        CONCLUSIÓ: T = 1   #
#############################