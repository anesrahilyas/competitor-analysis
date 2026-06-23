"""
pages/2_Visualizations.py
=========================
Deuxième page : visualisations de données pour l'analyse concurrentielle.

On réutilise les données récupérées en page 1 (st.session_state["results_df"]).
La page propose (cf. Lab 2, partie C) :
    - un bar chart de la distribution des notes
    - le top des applications par nombre d'installations
    - un camembert (pie chart) Apps gratuites vs payantes
    - un nuage de mots (word cloud) à partir des descriptions
Une barre latérale (sidebar) permet de filtrer les données par Application ID.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

st.title("📈 Data Visualizations")

# --- Vérification de la présence de données ---------------------------------
if "results_df" not in st.session_state:
    st.warning("Aucune donnée. Lancez d'abord une recherche dans « Results Table ».")
    st.stop()  # Interrompt l'exécution de la page proprement.

df: pd.DataFrame = st.session_state["results_df"].copy()
st.caption(f"Analyse concurrentielle pour : « {st.session_state.get('search_term', '')} »")

# --- Barre latérale : filtre par Application ID -----------------------------
st.sidebar.header("Filtres")
all_ids = df["appId"].dropna().tolist()
selected_ids = st.sidebar.multiselect(
    "Filtrer par Application ID",
    options=all_ids,
    default=all_ids,
    help="Sélectionnez les applications à inclure dans les graphiques.",
)
if selected_ids:
    df = df[df["appId"].isin(selected_ids)]

if df.empty:
    st.warning("Aucune application sélectionnée dans les filtres.")
    st.stop()

# Thème graphique homogène.
sns.set_theme(style="whitegrid")

# --- Ligne 1 : distribution des notes + top installations ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution des notes")
    scores = df["score"].dropna()
    if scores.empty:
        st.info("Pas de données de note disponibles.")
    else:
        fig, ax = plt.subplots()
        sns.histplot(scores, bins=10, kde=True, ax=ax, color="#4C9BE0")
        ax.set_xlabel("Note (/5)")
        ax.set_ylabel("Nombre d'applications")
        st.pyplot(fig)

with col2:
    st.subheader("Top applications par installations")
    if "minInstalls" in df and df["minInstalls"].notna().any():
        top = df.dropna(subset=["minInstalls"]).nlargest(10, "minInstalls")
        fig, ax = plt.subplots()
        sns.barplot(data=top, y="title", x="minInstalls", ax=ax, color="#4C9BE0")
        ax.set_xlabel("Installations (min)")
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("Pas de données d'installations disponibles.")

# --- Ligne 2 : gratuit vs payant + top par note -----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Applications gratuites vs payantes")
    if "free" in df:
        counts = df["free"].map({True: "Gratuite", False: "Payante"}).value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts.values, labels=counts.index, autopct="%1.0f%%",
               colors=["#4C9BE0", "#F0A04C"], startangle=90)
        ax.axis("equal")  # cercle parfait
        st.pyplot(fig)
    else:
        st.info("Pas de donnée gratuit/payant.")

with col4:
    st.subheader("Top applications par note")
    rated = df.dropna(subset=["score"])
    if rated.empty:
        st.info("Pas de données de note disponibles.")
    else:
        top_rated = rated.nlargest(10, "score")
        fig, ax = plt.subplots()
        sns.barplot(data=top_rated, y="title", x="score", ax=ax, color="#7DC15F")
        ax.set_xlabel("Note (/5)")
        ax.set_ylabel("")
        st.pyplot(fig)

# --- Nuage de mots à partir des descriptions --------------------------------
st.subheader("Nuage de mots (descriptions)")
texts = " ".join(df["description"].dropna().astype(str).tolist())
if texts.strip():
    wc = WordCloud(width=1000, height=400, background_color="white").generate(texts)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("Pas de descriptions disponibles pour générer le nuage de mots.")
