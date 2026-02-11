# 💎 NEXUS INTELLIGENCE

### Plateforme d'Aide à la Décision Stratégique - Analyse Big Data

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Git](https://img.shields.io/badge/Git-Collaboration-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## 📋 Table des Matières

- [Présentation du Projet](#-présentation-du-projet)
- [Fonctionnalités Principales](#-fonctionnalités-principales)
- [Architecture Technique](#%EF%B8%8F-architecture-technique)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Équipe & Contributions](#-équipe--contributions)
- [Roadmap](#-roadmap)

---

## 📄 Présentation du Projet

**NEXUS INTELLIGENCE** est une application web interactive développée dans le cadre du module **Management Opérationnel (MBA ESG)**.

### 🎯 Objectifs Métier

L'application transforme des données brutes (Big Data) en **indicateurs stratégiques exploitables** pour les décideurs. Elle permet d'auditer la performance de catalogues de contenus digitaux via une interface "No-Code" intuitive.

**Cas d'usage actuels :**
- 🎬 **Netflix** : Analyse stratégique du catalogue vidéo (films/séries)
- 🎵 **Spotify** : Audit musical et analyse de performance commerciale

### 🌟 Valeur Ajoutée

- ✅ **Centralisation** : Consolidation de données hétérogènes (CSV) dans un entrepôt haute performance
- ✅ **Visualisation** : KPIs critiques (Rentabilité, Brand Safety, Viralité, Géostratégie)
- ✅ **Accessibilité** : Interface intuitive pour utilisateurs non-techniques
- ✅ **Performance** : Requêtage SQL In-Memory avec DuckDB (zéro latence)

---

## 🚀 Fonctionnalités Principales

### 1. 🧠 Nexus Core - Ingestion & Détection Intelligente

- **Upload Universel** : Interface drag-and-drop pour fichiers CSV
- **Auto-Détection** : Identification automatique du type de données (Netflix, Spotify Artists, Spotify Tracks)
- **Stockage Haute Performance** : DuckDB pour requêtage SQL ultra-rapide

### 2. 🎬 Module Stratégie Vidéo (Netflix)

**KPIs Décisionnels :**
- Ratio Films/Séries
- Volume total de contenus
- Pays leader par production

**Fonctionnalités Analytiques :**
- Filtres dynamiques par année
- Chronologie de production (Area Chart)
- Top 5 des pays producteurs (Bar Chart)
- Clause WHERE SQL dynamique pour analyses temporelles

### 3. 🎵 Module Audit Musical (Spotify)

**Gestion des Risques :**
- Taux de contenu explicite (Brand Safety)
- Analyse de conformité pour diffusion publique

**Performance Commerciale :**
- Popularité moyenne du catalogue
- Volume d'heures d'écoute estimé
- Filtre "Hit-Maker" (slider de popularité)

**Analyses Avancées :**
- Matrice Audio : Énergie vs Danceability (segmentation Clubbing/Détente)
- Leaderboard Artistes par followers
- Analyse croisée des attributs audio

---

## ⚙️ Architecture Technique

### Stack Technologique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Frontend** | Streamlit | Interface utilisateur interactive |
| **Backend** | Python 3.10+ | Logique métier et traitement de données |
| **Base de Données** | DuckDB | Entrepôt analytique In-Memory |
| **Visualisation** | Plotly | Graphiques interactifs |
| **Versioning** | Git/GitHub | Gestion du code source |

### Schéma d'Architecture

```
┌─────────────────┐
│   Upload CSV    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Auto-Détection  │ ◄── Analyse des colonnes SQL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DuckDB Store  │ ◄── Stockage In-Memory
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQL Analytics  │ ◄── Requêtes dynamiques
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Visualisation   │ ◄── Dashboards Plotly
└─────────────────┘
```

---

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- Git
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

#### 1. Cloner le dépôt

```bash
git clone https://github.com/AbdenourAchouri/Streamlit_DuckDB.git
cd Streamlit_DuckDB
```

#### 2. Basculer sur la branche feature

```bash
git checkout feature/kpi-integration
```

#### 3. Créer l'environnement virtuel (Recommandé)

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 5. ⚠️ Préparation des Données (Étape Critique)

Le fichier `tracks.csv` est volumineux (>100Mo) et a été compressé pour respecter les limites GitHub.

**Action requise :**
```bash
# Décompresser le fichier dataset.zip
cd data
unzip dataset.zip
cd ..
```

> **Note :** Sans cette étape, l'analyse Spotify Tracks ne fonctionnera pas.

#### 6. Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible sur : **http://localhost:8501**

---

## 💡 Utilisation

### Workflow Utilisateur

1. **Accueil** : Sélectionner le module d'analyse souhaité
2. **Upload** : Glisser-déposer un fichier CSV
3. **Auto-Détection** : Le système identifie automatiquement le type de données
4. **Configuration** : Appliquer des filtres (année, popularité, etc.)
5. **Analyse** : Consulter les KPIs et visualisations interactives
6. **Export** : Télécharger les insights (fonctionnalité à venir)

### Exemples de Cas d'Usage

**Exemple 1 : Audit Netflix**
```
Objectif : Analyser l'évolution du catalogue Netflix entre 2015 et 2020
→ Uploader netflix_titles.csv
→ Filtrer sur les années 2015-2020
→ Consulter le ratio Films/Séries par année
```

**Exemple 2 : Brand Safety Spotify**
```
Objectif : Calculer le taux de contenu explicite pour une diffusion publique
→ Uploader tracks.csv
→ Consulter le KPI "Contenu Explicite"
→ Filtrer les tracks avec popularité > 70
```

---

## 📁 Structure du Projet

```
Streamlit_DuckDB/
│
├── app.py                      # Point d'entrée de l'application
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation du projet
│
├── data/                       # Jeux de données
│   ├── netflix_titles.csv
│   ├── artists.csv
│   ├── tracks.zip              # ⚠️ À décompresser
│   └── tracks.csv              # (généré après décompression)
│
├── modules/                    # Modules métier
│   ├── __init__.py
│   ├── nexus_core.py          # Auto-détection & DuckDB
│   ├── netflix_dashboard.py   # Module Netflix
│   └── spotify_dashboard.py   # Module Spotify
│
├── assets/                     # Ressources visuelles
│   └── logo.png
│
└── docs/                       # Documentation technique
    └── architecture.md
```

---

## 👥 Équipe & Contributions

Ce projet a été développé selon une méthodologie **Agile** avec répartition claire des responsabilités.

### Membres de l'Équipe

| Membre | Rôle | Contributions Principales |
|--------|------|---------------------------|
| **👤 Abdenour ACHOURI** | Lead Tech & Architecture | • Initialisation Git & gestion des branches<br>• Architecture Backend (Python/Streamlit)<br>• Intégration DuckDB<br>• Logique d'auto-détection CSV |
| **👤 Augustin AMIEL** | Product Owner & UI Design | • Conception UX/UI et design "Nexus"<br>• Développement Dashboard Netflix<br>• Intégration graphiques Plotly<br>• Documentation technique et métier |
| **👤 Fares FOUASSI** | Data Analyst & QA | • Analyse datasets et définition KPIs<br>• Dashboards Spotify (Tracks & Artists)<br>• Filtres dynamiques et SQL analytique<br>• Tests fonctionnels et recette qualité |

### Workflow Git

```
main (stable)
  │
  └── feature/kpi-integration (développement actif)
        │
        ├── Modules Netflix & Spotify
        ├── Auto-détection CSV
        └── KPIs stratégiques
```

**Prochaine étape :** Merge de `feature/kpi-integration` vers `main` après validation de la Pull Request.


## 🗺️ Roadmap

### ✅ Version Actuelle (v1.0 - Feature Branch)

- [x] Auto-détection de fichiers CSV
- [x] Dashboard Netflix complet
- [x] Dashboard Spotify (Tracks & Artists)
- [x] KPIs stratégiques (Brand Safety, Popularité, Géostratégie)
- [x] Filtres dynamiques interactifs

### 🚧 Prochaines Fonctionnalités (v1.1)

- [ ] Export des rapports en PDF
- [ ] Comparaisons multi-catalogues
- [ ] Alertes automatiques (seuils de KPI)
- [ ] Support de nouvelles sources de données (YouTube, Apple Music)
- [ ] API REST pour intégration externe
- [ ] Mode collaboratif (partage de dashboards)

### 🔮 Vision Long Terme (v2.0)

- [ ] Intelligence Artificielle prédictive (tendances de popularité)
- [ ] Recommandations stratégiques automatisées
- [ ] Intégration d'APIs temps réel
- [ ] Mode multi-utilisateurs avec authentification

---

## 📝 Licence

Ce projet a été développé dans un cadre académique (MBA ESG - Management Opérationnel).

© 2024 - Équipe NEXUS INTELLIGENCE

---


<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**

Made with ❤️ by Team NEXUS

</div>