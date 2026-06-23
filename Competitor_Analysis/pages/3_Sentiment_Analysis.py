"""
pages/3_Sentiment_Analysis.py
=============================
Troisième page : analyse de sentiment (application ML) basée sur un modèle
pré-entraîné HuggingFace (cf. Lab 2, partie D).

Pour chaque application issue de la recherche (page 1), on :
    1. récupère un échantillon d'avis utilisateurs,
    2. calcule le sentiment de chaque avis (positive / neutral / negative),
    3. calcule un score de sentiment global par application.

La page affiche un bar chart du score de sentiment de toutes les applications,
puis le détail des avis d'une application sélectionnée.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

import utils

st.set_page_config(page_title="Sentiment Analysis", page_icon="💬", layout="wide")

st.title("💬 Sentiment Analysis")

# --- Vérification des données ------------------------------------------------
if "results_df" not in st.session_state:
    st.warning("Aucune donnée. Lancez d'abord une recherche dans « Results Table ».")
    st.stop()

df: pd.DataFrame = st.session_state["results_df"]
st.caption(f"Analyse de sentiment pour : « {st.session_state.get('search_term', '')} »")

st.write(
    "On utilise un modèle de classification de texte pré-entraîné "
    f"(`{utils.SENTIMENT_MODEL}`) pour évaluer le sentiment des avis."
)

# Nombre d'avis à analyser par application (curseur dans la sidebar).
st.sidebar.header("Paramètres")
n_reviews = st.sidebar.slider("Avis à analyser par appli", 20, 150, 60, step=10)

# --- Calcul du score de sentiment pour toutes les applications --------------
if st.button("🚀 Lancer l'analyse de sentiment"):
    scores = []
    progress = st.progress(0.0, text="Analyse en cours...")
    app_ids = df["appId"].dropna().tolist()

    for i, app_id in enumerate(app_ids):
        result = utils.compute_app_sentiment(app_id, count=n_reviews)
        title = df.loc[df["appId"] == app_id, "title"].values
        scores.append({
            "appId": app_id,
            "title": title[0] if len(title) else app_id,
            "sentiment_score": result["score"],
            "n_reviews": result["n_reviews"],
        })
        progress.progress((i + 1) / len(app_ids),
                          text=f"Analyse : {i + 1}/{len(app_ids)} applications")

    progress.empty()
    # Persistance du résultat pour ne pas tout recalculer ensuite.
    st.session_state["sentiment_df"] = pd.DataFrame(scores)

# --- Affichage du bar chart global ------------------------------------------
if "sentiment_df" in st.session_state:
    sent_df = st.session_state["sentiment_df"]
    sent_df = sent_df[sent_df["n_reviews"] > 0]  # on ignore les apps sans avis

    st.subheader("Score de sentiment par application (0 = négatif, 100 = positif)")
    if sent_df.empty:
        st.info("Aucun avis disponible pour les applications trouvées.")
    else:
        sns.set_theme(style="whitegrid")
        ordered = sent_df.sort_values("sentiment_score", ascending=False)
        fig, ax = plt.subplots(figsize=(10, max(3, 0.4 * len(ordered))))
        sns.barplot(data=ordered, y="title", x="sentiment_score",
                    ax=ax, palette="RdYlGn")
        ax.set_xlim(0, 100)
        ax.set_xlabel("Score de sentiment")
        ax.set_ylabel("")
        st.pyplot(fig)

        # --- Détail des avis d'une application sélectionnée -----------------
        st.subheader("Détail des avis d'une application")
        choice = st.selectbox(
            "Choisir une application",
            options=ordered["appId"].tolist(),
            format_func=lambda aid: ordered.loc[ordered["appId"] == aid, "title"].values[0],
        )
        if choice:
            detail = utils.compute_app_sentiment(choice, count=n_reviews)
            reviews_df = detail["reviews_df"]

            c1, c2 = st.columns(2)
            c1.metric("Score de sentiment", f"{detail['score']} / 100")
            c2.metric("Avis analysés", detail["n_reviews"])

            if not reviews_df.empty:
                # Répartition positive / neutral / negative
                dist = reviews_df["label"].value_counts()
                fig, ax = plt.subplots()
                colors = {"positive": "#7DC15F", "neutral": "#F0C04C",
                          "negative": "#E0644C"}
                ax.bar(dist.index, dist.values,
                       color=[colors.get(l, "#999") for l in dist.index])
                ax.set_ylabel("Nombre d'avis")
                st.pyplot(fig)

                # Tableau détaillé des avis
                st.dataframe(reviews_df, use_container_width=True, hide_index=True)
            else:
                st.info("Aucun avis disponible pour cette application.")
else:
    st.info("Cliquez sur « Lancer l'analyse de sentiment » pour démarrer.")
