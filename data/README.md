# 💎 NEXUS INTELLIGENCE | Plateforme d'Aide à la Décision Stratégique

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Git](https://img.shields.io/badge/Git-Collaboration-F05032?style=for-the-badge&logo=git&logoColor=white)

## 📄 Présentation du Projet

**NEXUS INTELLIGENCE** est une application web interactive développée dans le cadre du module **Management Opérationnel (MBA ESG)**.

L'objectif est de transformer des données brutes (Big Data) en **indicateurs stratégiques** clairs pour les décideurs.  
L'application permet d'auditer la performance de catalogues de contenus digitaux (**Netflix** et **Spotify**) via une interface **No-Code** intuitive.

### 🎯 Objectifs Métier

- **Centraliser** l'analyse de données hétérogènes (CSV) dans un entrepôt local performant (DuckDB)
- **Visualiser** les KPIs critiques : Rentabilité, Brand Safety, Viralité, Géostratégie
- **Faciliter** la prise de décision grâce au Data Storytelling

---

## ⚙️ Instructions d'Installation et d'Exécution

Suivez ces étapes pour lancer l'application en local.

### 1. Cloner le dépôt Git

```bash
git clone https://github.com/atifrani/mgt_opl_env_dev.git
cd mgt_opl_env_dev

2. Créer l'environnement virtuel (Recommandé)

# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate

3. Installer les dépendances

pip install -r requirements.txt

4. Préparation des Données (⚠️ Étape Critique)

Le dossier data/ contient les jeux de données nécessaires aux tests.

Important :
Le fichier tracks.csv étant volumineux (>100 Mo), il a été compressé afin de respecter les limites de GitHub.

👉 Action requise :
Dézippez le fichier suivant :

data/tracks.zip

afin d’obtenir :

data/tracks.csv

Sans cette étape, le module Spotify Tracks ne pourra pas fonctionner.
5. Lancer l'application

streamlit run app.py

L'application sera accessible à l’adresse :

http://localhost:8501

🚀 Description des Fonctionnalités

L’application est construite autour de trois modules stratégiques majeurs.
🧠 1. Nexus Core — Ingestion & Détection

    Upload universel de fichiers CSV (glisser-déposer)

    Auto-détection du type de dataset :

        Netflix

        Spotify Artists

        Spotify Tracks

    Stockage haute performance via DuckDB

    Requêtes SQL In-Memory (zéro latence)

🎬 2. Module Stratégie Vidéo — Netflix

KPIs Décisionnels

    Ratio Films / Séries

    Volume total de contenus

    Pays producteurs dominants

Filtres Dynamiques

    Sélecteur d'année

    Clause SQL WHERE dynamique

Visualisations

    Chronologie de production (Area Chart)

    Géostratégie : Top 5 pays producteurs (Bar Chart)

🎵 3. Module Audit Musical — Spotify

Brand Safety

    Calcul du taux de contenu explicite

Performance Commerciale

    Popularité moyenne

    Volume global d’heures d’écoute

Filtres Avancés

    Slider Hit-Maker (ex : Top Hits > 80)

Analyse Audio

    Matrice Énergie vs Danceability

    Segmentation (Clubbing / Détente)

Leaderboard Artistes

    Classement par nombre de followers

👥 Répartition des Tâches — Équipe Projet
Membre	Rôle	Responsabilités
👤 Abdenour ACHOURI	Lead Tech & Architecture	Git & branches, backend Python/Streamlit, DuckDB, auto-détection CSV
👤 Augustin AMIEL	Product Owner & UI	UX/UI, Dashboard Netflix, Plotly, documentation
👤 Fares FOUASSI	Data Analyst & QA	KPIs métier, Dashboards Spotify, SQL analytique, tests
📌 Technologies Utilisées

    Python 3.10+

    Streamlit

    DuckDB

    Pandas

    Plotly

    Git & GitHub

📜 Licence & Contexte

Projet réalisé dans un cadre académique — MBA ESG.
Usage non commercial.

💎 NEXUS INTELLIGENCE
Transformer la donnée en décision stratégique