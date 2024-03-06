import streamlit as st
from us_recomender import *
import random
import numpy as np

# Título de la aplicación
st.title("Recomanador de llibres CBR")

def mapejar_ordre_usuari(generes_bd, ordre_usuari):
    # Crear un diccionari per a mapejar l'ordre de l'usuari
    dicc_ordre_usuari = {genere: ordre + 1 for ordre, genere in enumerate(ordre_usuari)}

    # Mapejar l'ordre de la base de dades a l'ordre de l'usuari
    ordre_mapejat = [str(dicc_ordre_usuari.get(genere, 0)) for genere in generes_bd]

    return ordre_mapejat

# Inicia un formulario
with st.form("Introdueix el teu perfil"):
    # Ordenació de gèneres
    
    generes_seleccionats = st.multiselect("Afegeix gèneres en l'ordre que prefereixis", generes)
    st.write('Tenint en compte que es consideren el següents rangs de pàgines de llibres:')
    st.write(f"{str(longituds)[1:-1]}")

    long = st.select_slider(
        'Quina llargària de llibre prefereixes?',
        options=['molt curt', 'curt', 'mig', 'llarg', 'molt llarg'],key='mig')
    
    # Longitud mitjana de llibres
    longitud = random.randint(longituds[long][0], longituds[long][1])

    # Quantitat de llibres llegits
    books_read = st.number_input("Aproximació de llibres llegits en els últims 10 anys", min_value=0, max_value=500, step=1)
    books_read += random.randint(-10, 10)  # Factor aleatori
    books_read = np.clip(np.array(books_read),0,500)
    exig = st.select_slider(
        'Ets una persona molt exigent i crítica amb els llibres?',
        options=['molt poc', 'poc', 'punt just', 'bastant', 'molt'],key='punt just')
    exigencia = random.uniform(ratings[exig][0], ratings[exig][1])

    enviado = st.form_submit_button("Enviar")

if 'recomanacions_fetes' not in st.session_state:
    st.session_state.recomanacions_fetes = False
    st.session_state.llibres = []
    st.session_state.parametres = []
    st.session_state.valoracions = []

if len(generes_seleccionats) != len(generes):
    st.warning("Has d'afegir tots els gèneres per indicar l'ordre de preferència")
else:
    if not st.session_state.recomanacions_fetes:
        genere_puntuacions = mapejar_ordre_usuari(generes, generes_seleccionats)
        usuari = genere_puntuacions + [str(longitud),str(books_read),str(exigencia)]

        with st.spinner('Buscant els millors llibres per tu...'):
            recomanacions, rs, newcas, casos, dicc_most_sim, cas_dists, paths = recomana(usuari)
            st.session_state.parametres = [rs, newcas, casos, dicc_most_sim, cas_dists, paths]
            diccion = cargar_diccionario()
            st.session_state.llibres = [diccion[i] for i in recomanacions]

        st.session_state.recomanacions_fetes = True

    if st.session_state.recomanacions_fetes:
        st.write('Et recomanem els següents **tres llibres**:')
        llibres = st.session_state.llibres
        st.write(f':blue[{llibres[0]}]')
        st.write(f':green[{llibres[1]}]')
        st.write(f':orange[{llibres[2]}]')
        
        on = st.toggle('Vols valorar els llibres? (tindràs un 5% de descompte a la nostra web)')
        
        if on:
            missatge_boto = 'Enviar valoració'
            st.write("Valora els llibres del 0 al 5 tenint en compte que si no has llegit el llibre has de valorar 0")
            v1 = st.number_input(f"Valora el llibre :blue[{llibres[0]}]", min_value=0, max_value=5, step=1)
            v2 = st.number_input(f"Valora el llibre :green[{llibres[1]}]", min_value=0, max_value=5, step=1)
            v3 = st.number_input(f"Valora el llibre :orange[{llibres[2]}]", min_value=0, max_value=5, step=1)
            st.session_state.valoracions = [v1,v2,v3]
        else:
            missatge_boto = "Finalitzar sessió"
    if 'pagina_gracies' not in st.session_state:
        st.session_state.pagina_gracies = False

    # Botó per enviar valoració
    enviar_valoracio = st.button(missatge_boto)

    if enviar_valoracio:
        st.session_state.pagina_gracies = True

    # Si l'usuari ha premut el botó, mostra la pàgina de gratitud
    if st.session_state.pagina_gracies:
        codi = random.randint(1000,9999)
        codi = f'BK{codi}'
        rs, newcas, casos, dicc_most_sim, cas_dists, paths = st.session_state.parametres
        if on:
            st.write("## Moltes gràcies per la seva valoració!")
            st.write(f"    Amb el codi {codi} tindrà un 5% de descompte a la nostra web")
            revise_retain(rs, newcas, casos, dicc_most_sim, cas_dists, paths,True,st.session_state.valoracions)
        else:
            st.write("## Moltes gràcies per confiar en nosaltres!")
            revise_retain(rs, newcas, casos, dicc_most_sim, cas_dists, paths,False)
