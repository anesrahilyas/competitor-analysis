"""
utils.py
========
Module utilitaire de l'application "Competitor Analysis".

Il regroupe TOUTES les fonctions de récupération et de traitement de données :
    - Recherche d'applications sur le Google Play Store (code API du Lab 1)
    - Récupération des avis (reviews) d'une application
    - Analyse de sentiment des avis via un modèle pré-entraîné HuggingFace

On utilise la librairie `google-play-scraper` qui encapsule l'API du
Play Store (voir Lab 1, partie 2 "Extracting Data using an API").

Toutes les fonctions "lentes" (appels réseau, chargement de modèle ML)
sont mises en cache avec les décorateurs Streamlit pour éviter de relancer
le calcul à chaque interaction de l'utilisateur.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from google_play_scraper import search, app, reviews, Sort


# ---------------------------------------------------------------------------
# 1. RECHERCHE D'APPLICATIONS (réutilisation du code API du Lab 1)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def search_apps(search_term: str, n_hits: int = 20,
                lang: str = "en", country: str = "us") -> pd.DataFrame:
    """
    Recherche des applications sur le Google Play Store à partir d'un terme.

    Pour chaque résultat de recherche, on appelle `app()` afin de récupérer
    les informations détaillées (note, nombre d'avis, installations, prix...).

    Paramètres
    ----------
    search_term : str
        Le terme de recherche saisi par l'utilisateur (ex: "note taking ai").
    n_hits : int
        Nombre maximum d'applications à récupérer.
    lang, country : str
        Langue et pays utilisés pour interroger le store.

    Retour
    ------
    pandas.DataFrame
        Un tableau avec une ligne par application et les colonnes utiles
        pour la suite (visualisations + analyse de sentiment).
    """
    # Étape 1 : recherche simple -> liste de hits (peu d'infos par hit)
    hits = search(search_term, lang=lang, country=country, n_hits=n_hits)

    rows = []
    for hit in hits:
        app_id = hit.get("appId")
        if not app_id:
            continue
        try:
            # Étape 2 : on enrichit chaque résultat avec les détails complets.
            # On gère les exceptions car certaines applis peuvent être
            # indisponibles ou bloquées selon le pays (bonne pratique Lab 1).
            details = app(app_id, lang=lang, country=country)
        except Exception:
            # Si le détail échoue, on retombe sur les infos basiques du hit.
            details = hit

        rows.append({
            "appId": app_id,
            "title": details.get("title"),
            "developer": details.get("developer"),
            "score": details.get("score"),               # note moyenne /5
            "ratings": details.get("ratings"),           # nb de notes
            "reviews": details.get("reviews"),           # nb d'avis
            "installs": details.get("installs"),         # ex: "1,000,000+"
            "minInstalls": details.get("minInstalls"),   # version numérique
            "free": details.get("free"),                 # True / False
            "price": details.get("price"),               # 0.0 si gratuit
            "genre": details.get("genre"),               # catégorie
            "released": details.get("released"),
            "description": details.get("description"),
            "icon": details.get("icon"),
            "url": details.get("url"),
        })

    df = pd.DataFrame(rows)
    return df


# ---------------------------------------------------------------------------
# 2. RÉCUPÉRATION DES AVIS D'UNE APPLICATION (pour l'analyse de sentiment)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_reviews(app_id: str, count: int = 80,
                lang: str = "en", country: str = "us") -> list[str]:
    """
    Récupère un échantillon d'avis utilisateurs pour une application donnée.

    On prend un sous-ensemble représentatif (les avis les plus pertinents),
    ce qui est suffisant pour l'analyse de sentiment (cf. Lab 2, partie D).

    Paramètres
    ----------
    app_id : str
        L'identifiant de l'application (ex: "com.exemple.app").
    count : int
        Nombre d'avis à récupérer.

    Retour
    ------
    list[str]
        La liste du contenu textuel des avis (les textes vides sont filtrés).
    """
    try:
        result, _ = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.MOST_RELEVANT,
            count=count,
        )
    except Exception:
        # En cas d'erreur réseau / appli sans avis, on renvoie une liste vide.
        return []

    # On ne garde que le texte non vide des avis.
    return [r["content"] for r in result if r.get("content")]


# ---------------------------------------------------------------------------
# 3. ANALYSE DE SENTIMENT (TextBlob - NLP léger)
# ---------------------------------------------------------------------------
# On utilise TextBlob qui fournit une analyse de sentiment basée sur un
# lexique (polarity entre -1 et +1). C'est léger, rapide, et ne nécessite
# pas de télécharger un modèle de plusieurs Go.
SENTIMENT_METHOD = "TextBlob"


def analyze_reviews(review_texts: list[str]) -> pd.DataFrame:
    """
    Calcule le sentiment de chaque avis avec TextBlob.

    TextBlob attribue un score de polarité entre -1 (très négatif) et +1
    (très positif). On catégorise :
        - polarity > 0.1  -> positive
        - polarity < -0.1 -> negative
        - sinon           -> neutral

    Retour
    ------
    pandas.DataFrame
        Colonnes : review, label (positive/neutral/negative), confidence.
    """
    from textblob import TextBlob

    if not review_texts:
        return pd.DataFrame(columns=["review", "label", "confidence"])

    rows = []
    for text in review_texts:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # entre -1 et +1

        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"

        # La "confidence" est l'intensité absolue de la polarité (0 à 1).
        confidence = round(abs(polarity), 3)
        rows.append({
            "review": text,
            "label": label,
            "confidence": confidence,
        })
    return pd.DataFrame(rows)


def sentiment_score(reviews_df: pd.DataFrame) -> float:
    """
    Calcule un score de sentiment global pour une application, sur 0 à 100.

    Méthode : on associe positive=+1, neutral=0, negative=-1, on fait la
    moyenne puis on remet l'échelle entre 0 (très négatif) et 100 (très positif).
    """
    if reviews_df.empty:
        return 0.0

    mapping = {"positive": 1, "neutral": 0, "negative": -1}
    numeric = reviews_df["label"].map(mapping).fillna(0)
    mean = numeric.mean()                 # entre -1 et +1
    return round((mean + 1) / 2 * 100, 1)  # entre 0 et 100


@st.cache_data(show_spinner=False)
def compute_app_sentiment(app_id: str, count: int = 80) -> dict:
    """
    Pipeline complet pour une application :
        avis -> sentiment de chaque avis -> score global de l'appli.

    Retour
    ------
    dict
        {"app_id", "n_reviews", "score", "reviews_df"}
    """
    review_texts = get_reviews(app_id, count=count)
    reviews_df = analyze_reviews(review_texts)
    return {
        "app_id": app_id,
        "n_reviews": len(review_texts),
        "score": sentiment_score(reviews_df),
        "reviews_df": reviews_df,
    }
