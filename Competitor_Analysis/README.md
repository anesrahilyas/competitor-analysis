# Competitor Analysis — Streamlit App (Lab 2)

Application Streamlit multi-pages d'analyse concurrentielle d'applications mobiles,
basée sur les données du **Google Play Store** (API `google-play-scraper`, réutilisée du Lab 1).

## Fonctionnalités
- **Recherche d'apps** à partir d'un terme saisi par l'utilisateur.
- **Tableau de résultats** (notes, installations, genre, gratuit/payant...).
- **Visualisations** : distribution des notes, top installations, gratuit vs payant, nuage de mots.
- **Analyse de sentiment** des avis utilisateurs via un modèle pré-entraîné HuggingFace.

## Structure du projet
```
Competitor_Analysis/
├── Home.py                       # Page d'accueil (point d'entrée)
├── utils.py                      # Fonctions API + ML (recherche, avis, sentiment)
├── test_app.py                   # Bac à sable des widgets (section B du lab)
├── requirements.txt              # Dépendances
├── .streamlit/
│   └── config.toml               # Thème de l'app
└── pages/
    ├── 1_Results_Table.py        # Recherche + tableau de résultats
    ├── 2_Visualizations.py       # Graphiques d'analyse concurrentielle
    └── 3_Sentiment_Analysis.py   # Analyse de sentiment des avis
```

## Installation et lancement
```bash
# 1. (Recommandé) activer votre environnement virtuel du Lab 1
conda activate <votre_env>

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run Home.py
```

## Notes
- La persistance des données entre pages se fait via `st.session_state` :
  lancez d'abord une recherche sur la page **Results Table**.
- Le modèle de sentiment (`transformers` + `torch`) est téléchargé au premier
  usage : la première analyse peut donc être un peu longue.

## Pistes d'amélioration
- Ajouter des sources de données (ProductHunt, GitHub) — cf. Lab 1.
- Visualisations plus riches (heatmaps, box plots).
- Analyse comparative ou fonctionnalités basées sur un LLM.
