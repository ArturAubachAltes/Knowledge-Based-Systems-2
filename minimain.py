from miniCBR import *
import pandas as pd

df_problemes = pd.read_csv('./data/problems4000(real).csv')
df_problemes.drop('Unnamed: 0',axis=1,inplace=True)
rs = createRS(casebase=df_problemes, maxcasesxleaf=10)

# Exemple de prova: [1,0,0,0,0,0.3,0,0,0,0,0.5,0.5,0.5]

while True:
    newp = Problem(*eval(input('Introdueix la nova instancia de Problem(): ')))
    newcas = Cas(id=(len(rs.indexacio)),descripcio=rs.scaler.transform([newp.array])[0])

    distance, case, path = rs.retrieve(newcas)
    rs.reuse(case, newcas)
    rs.revise(newcas)
    rs.retain(distance, newcas, path)

    exit = eval(input('Vols seguir amb una nova recomanació? (True/False): '))
    if not exit:
        break


