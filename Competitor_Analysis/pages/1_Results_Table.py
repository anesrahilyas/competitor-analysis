"""
pages/1_Results_Table.py
=========================
Première page : saisie du terme de recherche par l'utilisateur, appel de la
fonction de recherche (utils.search_apps) et affichage des résultats dans un
tableau (dataframe).

Les résultats sont stockés dans `st.session_state` afin d'être PERSISTÉS et
réutilisés par les autres pages (Visualizations, Sentiment Analysis).
Voir Lab 2, partie C : "persist data across pages" / "session state".
"""

import streamlit as st

import utils

st.set_page_config(page_title="Results Table", page_icon="📋", layout="wide")

st.title("📋 Search & Results")

# --- Formulaire de recherche -------------------------------------------------
with st.form("search_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        # Terme de recherche libre (le sujet demande de laisser l'utilisateur
        # choisir son propre terme, contrairement au Lab 1 figé).
        search_term = st.text_input(
            "Search term",
            value="note taking ai",
            help="Entrez un mot-clé pour rechercher des applications.",
        )
    with col2:
        n_hits = st.number_input(
            "Number of apps", min_value=5, max_value=50, value=20, step=5
        )
    submitted = st.form_submit_button("🔍 Search")

# --- Lancement de la recherche ----------------------------------------------
if submitted and search_term.strip():
    # st.spinner améliore l'expérience utilisateur pendant l'appel réseau.
    with st.spinner(f"Recherche d'applications pour « {search_term} »..."):
        df = utils.search_apps(search_term.strip(), n_hits=int(n_hits))

    if df.empty:
        st.warning("Aucun résultat trouvé. Essayez un autre terme de recherche.")
    else:
        # On persiste les données et le terme pour les autres pages.
        st.session_state["results_df"] = df
        st.session_state["search_term"] = search_term.strip()
        st.success(f"{len(df)} applications trouvées pour « {search_term} ».")

# --- Affichage des résultats persistés --------------------------------------
if "results_df" in st.session_state:
    df = st.session_state["results_df"]

    st.subheader(f"Résultats : {st.session_state.get('search_term', '')}")

    # Quelques métriques rapides en haut de page.
    m1, m2, m3 = st.columns(3)
    m1.metric("Applications", len(df))
    m2.metric("Note moyenne", f"{df['score'].mean():.2f} / 5"
              if df["score"].notna().any() else "N/A")
    free_ratio = (df["free"].sum() / len(df) * 100) if "free" in df else 0
    m3.metric("Apps gratuites", f"{free_ratio:.0f} %")

    # Affichage du tableau avec configuration de colonnes (column_config).
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "icon": st.column_config.ImageColumn("Icône"),
            "url": st.column_config.LinkColumn("Lien Play Store"),
            "score": st.column_config.NumberColumn("Note", format="%.2f ⭐"),
            "description": st.column_config.TextColumn("Description", width="medium"),
        },
    )

    # Permettre le téléchargement des données en CSV (download_button).
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Télécharger les résultats (CSV)",
        data=csv,
        file_name="competitor_results.csv",
        mime="text/csv",
    )
else:
    st.info("Lancez une recherche ci-dessus pour afficher les résultats.")
