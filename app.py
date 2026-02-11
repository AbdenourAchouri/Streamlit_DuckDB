import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import duckdb
from utils.db import get_connection

# --- 1. CONFIGURATION GLOBALE ---
st.set_page_config(
    page_title="NEXUS Intelligence",
    page_icon="💎",
    layout="wide"
)

# --- 2. CSS "PREMIUM" (Design Vendeur & Lisible) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    body {font-family: 'Inter', sans-serif; background-color: #f8fafc;}

    /* TITRE PRINCIPAL - STYLE "BIG TECH" */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: -webkit-linear-gradient(90deg, #2563eb, #1e40af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 20px;
    }
    
    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 40px;
    }

    /* CARTES KPI (Storytelling) */
    .kpi-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .kpi-label { font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.5px; }
    .kpi-value { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 5px 0; }
    .kpi-insight { font-size: 0.85rem; color: #3b82f6; font-weight: 500; border-top: 1px solid #f1f5f9; padding-top: 8px; margin-top: 8px;}

    /* BLOC ÉQUIPE (Centré & Pro) */
    .team-box {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        text-align: center;
        margin: 30px auto;
        max-width: 700px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .team-label { color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-weight: bold;}
    .team-names { 
        display: flex; justify-content: center; gap: 30px; 
        font-weight: 600; color: #334155; font-size: 1rem; flex-wrap: wrap;
    }
    
    /* Upload Zone */
    div[data-testid="stFileUploader"] {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTIONS BACKEND (ROBUSTES) ---

def load_data(file):
    try:
        return pd.read_csv(file, encoding='utf-8')
    except:
        return pd.read_csv(file, encoding='latin-1')

def detect_dataset_type(con):
    """Détection intelligente via SQL"""
    # On récupère les colonnes en minuscule
    columns_info = con.execute("DESCRIBE data").fetchall()
    cols = [c[0].lower() for c in columns_info]
    
    if 'show_id' in cols and 'type' in cols:
        return 'NETFLIX'
    elif 'followers' in cols and ('genres' in cols or 'genre' in cols):
        return 'SPOTIFY_ARTISTS'
    # Détection plus souple pour les tracks
    elif 'danceability' in cols and 'energy' in cols:
        return 'SPOTIFY_TRACKS'
    return 'UNKNOWN'

# --- 4. DASHBOARDS MÉTIER ---

def render_netflix_strategy(con):
    st.markdown("### 🎬 Performance du Catalogue Netflix")
    st.markdown("---")
    
    # --- FILTRE DYNAMIQUE ---
    st.sidebar.header("🎚️ Filtres")
    years = [x[0] for x in con.execute("SELECT DISTINCT release_year FROM data ORDER BY 1 DESC").fetchall()]
    selected_year = st.sidebar.selectbox("Année de Sortie", ["Toutes les années"] + years)
    
    where_clause = "WHERE 1=1"
    if selected_year != "Toutes les années":
        where_clause += f" AND release_year = {selected_year}"

    # --- KPIs SQL ---
    df_type = con.execute(f"SELECT type, COUNT(*) as cnt FROM data {where_clause} GROUP BY type").df()
    total = df_type['cnt'].sum()
    if total == 0: total = 1 
    
    nb_movies = df_type[df_type['type']=='Movie']['cnt'].sum()
    movie_pct = (nb_movies / total) * 100
    
    top_country = con.execute(f"SELECT country FROM data {where_clause} AND country IS NOT NULL GROUP BY country ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_c_name = top_country[0].split(',')[0] if top_country else "N/A"

    # AFFICHAGE
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="kpi-card"><div class="kpi-label">Volume Total</div><div class="kpi-value">{total:,}</div><div class="kpi-insight">Titres analysés</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card"><div class="kpi-label">Ratio Films</div><div class="kpi-value">{movie_pct:.0f}%</div><div class="kpi-insight">vs Séries TV</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card"><div class="kpi-label">Pays Leader</div><div class="kpi-value">{top_c_name}</div><div class="kpi-insight">Production majeure</div></div>""", unsafe_allow_html=True)
    
    # Indicateur Stratégique
    strategy = "Cinéma" if movie_pct > 50 else "Télévision"
    c4.markdown(f"""<div class="kpi-card"><div class="kpi-label">Stratégie</div><div class="kpi-value" style="font-size: 1.5rem; margin-top: 10px; margin-bottom: 10px;">{strategy}</div><div class="kpi-insight">Positionnement</div></div>""", unsafe_allow_html=True)

    # GRAPHIQUES
    st.markdown("<br>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        st.subheader("📈 Évolution Chronologique")
        df_evo = con.execute(f"SELECT release_year, type, COUNT(*) as count FROM data {where_clause} GROUP BY release_year, type ORDER BY release_year").df()
        fig = px.area(df_evo, x='release_year', y='count', color='type', template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_g2:
        st.subheader("🌍 Top 5 Pays")
        df_pays = con.execute(f"SELECT country, COUNT(*) as count FROM data {where_clause} AND country IS NOT NULL GROUP BY country ORDER BY count DESC LIMIT 5").df()
        fig = px.bar(df_pays, x='count', y='country', orientation='h', color='count', 
                     template="plotly_white", color_continuous_scale='Blues') 
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

def render_spotify_tracks_strategy(con):
    st.markdown("### 🎵 Audit du Catalogue Musical (Tracks)")
    st.markdown("---")
    
    # --- FILTRE DYNAMIQUE (Slider) ---
    st.sidebar.header("🎚️ Filtres")
    min_pop, max_pop = con.execute("SELECT MIN(popularity), MAX(popularity) FROM data").fetchone()
    if min_pop is None: min_pop, max_pop = 0, 100
    
    pop_range = st.sidebar.slider("Niveau de Popularité", int(min_pop), int(max_pop), (int(min_pop), int(max_pop)))
    where_clause = f"WHERE popularity BETWEEN {pop_range[0]} AND {pop_range[1]}"

    # --- KPIs Business ---
    # Gestion colonne Explicite
    cols = [x[0] for x in con.execute("DESCRIBE data").fetchall()]
    explicit_col = 'explicit' if 'explicit' in cols else 'NULL'
    
    # --- CORRECTION DU BUG ICI ---
    # On utilise TRY_CAST ou une conversion explicite pour éviter l'erreur "INT64 to string"
    # On compare tout en STRING pour être sûr
    kpi_query = f"""
        SELECT 
            COUNT(*) as total,
            AVG(popularity) as avg_pop,
            SUM(duration_ms)/1000/3600 as hours,
            SUM(CASE WHEN CAST({explicit_col} AS VARCHAR) IN ('true', 'True', '1') THEN 1 ELSE 0 END) as expl
        FROM data {where_clause}
    """
    stats = con.execute(kpi_query).fetchone()
    
    if not stats or stats[0] == 0:
        st.warning("Aucune donnée pour ce filtre.")
        return

    total, avg_pop, hours, explicit_count = stats
    if hours is None: hours = 0
    explicit_rate = (explicit_count / total * 100) if explicit_count else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="kpi-card"><div class="kpi-label">Volume Titres</div><div class="kpi-value">{total:,}</div><div class="kpi-insight">Titres sélectionnés</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card"><div class="kpi-label">Durée Catalogue</div><div class="kpi-value">{hours:.0f} h</div><div class="kpi-insight">Temps d'écoute</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card"><div class="kpi-label">Performance</div><div class="kpi-value">{avg_pop:.0f}/100</div><div class="kpi-insight">Score Moyen</div></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="kpi-card"><div class="kpi-label">Brand Safety</div><div class="kpi-value">{explicit_rate:.1f}%</div><div class="kpi-insight">Contenu Explicite</div></div>""", unsafe_allow_html=True)

    # VISUALISATIONS
    st.markdown("<br>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("📊 Distribution des Hits")
        df_hist = con.execute(f"SELECT popularity FROM data {where_clause}").df()
        fig = px.histogram(df_hist, x="popularity", nbins=20, color_discrete_sequence=['#1DB954'], template="plotly_white")
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.subheader("⏱️ Calibration (Durée)")
        df_dur = con.execute(f"SELECT duration_ms/60000 as minutes FROM data {where_clause} USING SAMPLE 1000").df()
        fig = px.box(df_dur, y="minutes", color_discrete_sequence=['#1e40af'], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # Matrice
    st.subheader("🔍 Matrice : Énergie vs Danse")
    # Gestion du nom de colonne 'name' vs 'track_name'
    if 'track_name' in cols: name_col = 'track_name'
    elif 'name' in cols: name_col = 'name'
    else: name_col = "''"

    df_scatter = con.execute(f"SELECT energy, danceability, popularity, {name_col} as titre FROM data {where_clause} USING SAMPLE 500").df()
    fig = px.scatter(df_scatter, x='energy', y='danceability', color='popularity', size='popularity',
                     hover_name='titre', template="plotly_white", color_continuous_scale='Viridis',
                     title="Positionnement Marketing (Club vs Chill)")
    st.plotly_chart(fig, use_container_width=True)

def render_spotify_artists_strategy(con):
    st.markdown("### 🎧 Leaderboard Artistes")
    st.markdown("---")
    
    # Correction type
    try: con.execute("ALTER TABLE data ALTER followers TYPE BIGINT") 
    except: pass

    stats = con.execute("SELECT COUNT(*), AVG(popularity) FROM data").fetchone()
    top_art = con.execute("SELECT name FROM data ORDER BY followers DESC LIMIT 1").fetchone()
    top_name = top_art[0] if top_art else "N/A"

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="kpi-card"><div class="kpi-label">Base Artistes</div><div class="kpi-value">{stats[0]:,}</div><div class="kpi-insight">Portfolio analysé</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card"><div class="kpi-label">Score Popularité</div><div class="kpi-value">{stats[1]:.1f}</div><div class="kpi-insight">Moyenne globale</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card"><div class="kpi-label">Top Influenceur</div><div class="kpi-value">{top_name}</div><div class="kpi-insight">Plus grosse base fan</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Top 10 Puissance (Followers)")
    df_top = con.execute("SELECT name, followers, popularity FROM data ORDER BY followers DESC LIMIT 10").df()
    
    fig = px.bar(df_top, x='followers', y='name', orientation='h', text_auto='.2s',
                 template="plotly_white", color='popularity', color_continuous_scale='Greens')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# --- 5. MAIN APP ---
def main():
    # HEADER
    st.markdown('<div class="main-title">NEXUS INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Plateforme d\'Aide à la Décision Stratégique</div>', unsafe_allow_html=True)

    # UPLOAD
    uploaded_file = st.file_uploader("📂 IMPORTER UN DATASET (CSV)", type=['csv'])

    # BLOC ÉQUIPE
    st.markdown("""
    <div class="team-box">
        <div class="team-label">Développé par</div>
        <div class="team-names">
            <span>Abdenour ACHOURI</span> • 
            <span>Augustin AMIEL</span> • 
            <span>Fares FOUASSI</span>
        </div>
        <div style="margin-top:10px; font-size: 0.8rem; color: #94a3b8;">MBA ESG - MBDIA</div>
    </div>
    """, unsafe_allow_html=True)

    # LOGIQUE PRINCIPALE
    if uploaded_file:
        df = load_data(uploaded_file)
        
        # Nettoyage header
        df.columns = [c.lower().strip().replace(" ", "_").replace(".", "") for c in df.columns]
        
        con = get_connection()
        con.execute("CREATE OR REPLACE TABLE data AS SELECT * FROM df")
        
        dtype = detect_dataset_type(con)
        
        if dtype == 'NETFLIX': render_netflix_strategy(con)
        elif dtype == 'SPOTIFY_ARTISTS': render_spotify_artists_strategy(con)
        elif dtype == 'SPOTIFY_TRACKS': render_spotify_tracks_strategy(con)
        else:
            st.warning("⚠️ Dataset non reconnu. Veuillez utiliser les fichiers Netflix ou Spotify (Artists/Tracks).")
            st.dataframe(df.head())

if __name__ == "__main__":
    main()