"""
test_app.py
-----------
Bac à sable de la SECTION B du Lab 2 : "Anatomy of a Streamlit Application".

Ce fichier n'est PAS l'application finale : c'est un terrain d'essai pour
découvrir les widgets, la "Streamlit Magic", et les éléments de layout.

Lancement :  streamlit run test_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Test Widgets", layout="wide")

# ---------------------------------------------------------------------------
# 1. WIDGETS D'AFFICHAGE (Display widgets)
# ---------------------------------------------------------------------------
st.title("Démo des widgets Streamlit")          # titre
st.header("1. Widgets d'affichage")             # en-tête
st.subheader("Texte, markdown, code, latex")    # sous-titre
st.text("Ceci est du texte brut.")
st.markdown("Ceci est du **markdown** avec du *style*.")
st.code("print('Hello Streamlit')", language="python")
st.latex(r"E = mc^2")

# ---------------------------------------------------------------------------
# 2. WIDGETS DE SAISIE (Input widgets)
# ---------------------------------------------------------------------------
st.header("2. Widgets de saisie")
nom = st.text_input("Votre nom")
age = st.number_input("Votre âge", min_value=0, max_value=120, value=25)
date = st.date_input("Une date")
if nom:
    st.write(f"Bonjour {nom}, vous avez {age} ans.")

# ---------------------------------------------------------------------------
# 3. WIDGETS DE FILTRE (Filters widgets)
# ---------------------------------------------------------------------------
st.header("3. Widgets de filtre")
accepte = st.checkbox("J'accepte les conditions")
choix = st.radio("Choisissez une option", ["A", "B", "C"])
ville = st.selectbox("Sélectionnez une ville", ["Paris", "Lyon", "Marseille"])
valeur = st.slider("Choisissez une valeur", 0, 100, 50)
multi = st.multiselect("Plusieurs choix", ["Python", "SQL", "Streamlit"])

# ---------------------------------------------------------------------------
# 4. WIDGETS BOUTON (Button widgets)
# ---------------------------------------------------------------------------
st.header("4. Boutons")
if st.button("Cliquez-moi"):
    st.success("Bouton cliqué !")

# ---------------------------------------------------------------------------
# 5. STREAMLIT MAGIC
# ---------------------------------------------------------------------------
# "Magic" : écrire une variable seule sur une ligne suffit à l'afficher,
# sans appeler explicitement st.write().
st.header("5. Streamlit Magic")
df = pd.DataFrame(
    np.random.randn(10, 3),
    columns=["A", "B", "C"],
)
df  # <-- Magic : ce DataFrame s'affiche tout seul dans l'app

# ---------------------------------------------------------------------------
# 6. WIDGETS DE DONNEES (Data widgets) + column_config
# ---------------------------------------------------------------------------
st.header("6. Widgets de données")
st.dataframe(df, use_container_width=True)   # tableau interactif
st.table(df.head(3))                          # tableau statique

# ---------------------------------------------------------------------------
# 7. LAYOUT & CONTAINERS (UX Design)
# ---------------------------------------------------------------------------
st.header("7. Layout et containers")
c1, c2 = st.columns(2)              # deux colonnes côte à côte
with c1:
    st.metric("Ventes", "1.2K", "+5%")
with c2:
    st.metric("Utilisateurs", "350", "-2%")

with st.expander("Cliquez pour voir plus de détails"):
    st.write("Contenu caché dans un container repliable (expander).")

# Sidebar : barre latérale (élément de layout)
st.sidebar.title("Barre latérale")
st.sidebar.write("Les widgets placés ici apparaissent à gauche.")
