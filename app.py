import streamlit as st
import pandas as pd
import duckdb
# Assure-toi que utils/db.py existe (voir étape 1)
from utils.db import get_connection 
import plotly.express as px # Plus joli que matplotlib pour le web

st.set_page_config(page_title="Dashboard Netflix/Spotify", layout="wide")

st.title("📊 Analyse Interactive : Netflix & Spotify")

# 1. Connexion DB
con = get_connection()

# 2. Upload et Chargement des données
st.sidebar.header("1. Chargement des données")
uploaded_file = st.sidebar.file_uploader("Téléverser votre CSV (Netflix ou Spotify)", type="csv")

if uploaded_file:
    # On charge le CSV dans un DataFrame Pandas d'abord
    df = pd.read_csv(uploaded_file)
    
    # Nettoyage basique des noms de colonnes (enlève les espaces, met en minuscule)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # Création de la table dans DuckDB (remplacement propre)
    con.execute("CREATE OR REPLACE TABLE data AS SELECT * FROM df")
    
    st.sidebar.success("Données chargées dans DuckDB !")
    
    # ---------------------------------------------------------
    # 3. Filtres Dynamiques (SQL WHERE)
    # ---------------------------------------------------------
    st.sidebar.header("2. Filtres")
    
    # Détection automatique des colonnes pour les filtres
    # Exemple: Si c'est Netflix, on a 'release_year'. Si Spotify, 'year' ou 'released_year'.
    columns = [x[0] for x in con.execute("DESCRIBE data").fetchall()]
    
    # Filtre Année (Universel)
    year_col = 'release_year' if 'release_year' in columns else ('year' if 'year' in columns else None)
    
    if year_col:
        years = con.execute(f"SELECT DISTINCT {year_col} FROM data ORDER BY 1 DESC").df()
        selected_year = st.sidebar.selectbox("Sélectionner une année", years)
    else:
        selected_year = None

    # Filtre Type ou Genre
    type_col = 'type' if 'type' in columns else ('genre' if 'genre' in columns else None)
    selected_type = "Tous"
    if type_col:
        types = con.execute(f"SELECT DISTINCT {type_col} FROM data").df()
        type_list = ["Tous"] + types[type_col].tolist()
        selected_type = st.sidebar.selectbox("Sélectionner un Type/Genre", type_list)

    # ---------------------------------------------------------
    # 4. Construction de la requête SQL filtrée
    # ---------------------------------------------------------
    query = "SELECT * FROM data WHERE 1=1"
    
    if selected_year:
        query += f" AND {year_col} = {selected_year}"
    
    if selected_type != "Tous":
        query += f" AND {type_col} = '{selected_type}'"
        
    # Exécution de la requête filtrée
    filtered_df = con.execute(query).df()
    
    st.write(f"### Résultats ({len(filtered_df)} éléments trouvés)")
    st.dataframe(filtered_df.head())

    # ---------------------------------------------------------
    # 5. Les 4 KPIs (Indicateurs Clés)
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📈 Indicateurs Clés de Performance (KPI)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI 1 : Volume total
    col1.metric("Total Titres", len(filtered_df))
    
    # KPI 2 : Durée moyenne (Adaptation selon dataset)
    if 'duration_min' in filtered_df.columns: # Spotify
        avg_dur = filtered_df['duration_min'].mean()
        col2.metric("Durée Moyenne", f"{avg_dur:.2f} min")
    elif 'duration' in filtered_df.columns: # Netflix
        col2.metric("Durée info", "Variable") # Plus complexe à parser sur Netflix
    else:
        col2.metric("KPI 2", "N/A")

    # KPI 3 & 4 : Visualisations graphiques
    
    # Graphique 1 : Top 10 des catégories/genres
    st.subheader("Répartition par Catégorie")
    if type_col:
        chart_data = filtered_df[type_col].value_counts().reset_index()
        chart_data.columns = ['Categorie', 'Compte']
        st.bar_chart(chart_data.set_index('Categorie'))
    
    # Graphique 2 : Évolution temporelle (si pas filtré par année unique)
    st.subheader("Évolution dans le temps")
    if year_col and selected_year is None: # Si on regarde tout l'historique
        time_data = con.execute(f"SELECT {year_col}, COUNT(*) as count FROM data GROUP BY {year_col} ORDER BY {year_col}").df()
        st.line_chart(time_data.set_index(year_col))
    else:
        st.info("Désactivez le filtre d'année pour voir l'évolution temporelle.")

else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")