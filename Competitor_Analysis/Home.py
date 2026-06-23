"""
Home.py
=======
Page d'accueil de l'application Streamlit "Competitor Analysis".

C'est le point d'entrée de l'application (équivalent d'un README pour le projet).
On la lance avec :  streamlit run Home.py

Streamlit détecte automatiquement les fichiers du dossier `pages/` et crée
un menu de navigation sur la gauche.
"""

import streamlit as st

# st.set_page_config DOIT être la première commande Streamlit appelée.
st.set_page_config(
    page_title="Competitor Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("Competitor Analysis")

st.subheader("Overview")
st.write(
    "Ceci est un prototype rapide d'application d'analyse concurrentielle. "
    "À partir d'une requête de recherche, l'application fournit une analyse "
    "des applications mobiles du marché ciblé afin d'en tirer des insights "
    "concurrentiels (données issues du Google Play Store)."
)

# Deux colonnes : fonctionnalités à gauche, améliorations possibles à droite.
col_features, col_improvements = st.columns(2)

with col_features:
    st.subheader("Key Features")
    st.markdown(
        """
        - 🔍 **Search for Apps** : recherche d'applications par mot-clé
        - 📋 **Listing results** : affichage des résultats sous forme de tableau
        - 🧰 **Filtering / Sorting results** : filtres et tris interactifs
        - 📈 **Data visualizations** : graphiques pour l'analyse concurrentielle
        - 💬 **Sentiment Analysis** : analyse des avis utilisateurs
        """
    )

with col_improvements:
    st.subheader("Improvements")
    st.markdown(
        """
        - Enrichir les visualisations de données
        - Ajouter des sources (ProductHunt, GitHub...)
        - Réviser les fonctionnalités selon les retours
        """
    )

st.divider()

# Petit guide de navigation pour l'utilisateur.
st.info(
    "👈 Utilisez le menu de gauche pour naviguer :\n\n"
    "1. **Results Table** — lancez une recherche et consultez les résultats\n"
    "2. **Visualizations** — explorez les graphiques d'analyse concurrentielle\n"
    "3. **Sentiment Analysis** — analysez le sentiment des avis utilisateurs"
)

st.caption("Comment lancer : `streamlit run Home.py` dans l'environnement virtuel.")
