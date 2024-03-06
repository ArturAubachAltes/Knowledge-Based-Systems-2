from CBR import *

def recomana(user):
    """
       Donat un usuari, representat per una llista de strings, que contenen 
       la seva informació, crea unes recomanacions per aquest
       retornant una llista amb tres id de llibres
    """
    user = 'Problem('+' ,'.join(user)+')'
    newp = eval(user)
    rs = createRS(from_model=True,path='recomanador.pkl')
    
    most_similar_cases, newcas = rs.retrieve(newp)

    distancies, casos, paths = zip(*most_similar_cases)
    cas_dists = list(zip(distancies, casos))

    dicc_most_sim = rs.reuse(cas_dists, newcas)

    return list(dicc_most_sim.keys()), rs, newcas, casos, dicc_most_sim, cas_dists,paths

def revise_retain(rs,newcas,casos,dicc_most_sim,cas_dists,paths,user_avalua,evaluation=[]):
    if user_avalua:
        rs.revise(newcas, casos, dicc_most_sim, user_avalua,evaluation)
    else:
        rs.revise(newcas, casos, dicc_most_sim, user_avalua)
    rs.retain(newcas, cas_dists, paths[0])
    # Comprovar si s'ha de realitzar un manteniment de la base de casos:
    if rs.cas_nr + rs.cas_r_u > 100:
        rs.maintenance()
    rs.save('recomanador')
