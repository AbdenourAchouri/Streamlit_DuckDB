# utils/db.py
import duckdb
import streamlit as st

# Singleton pattern : on ne se connecte qu'une seule fois
@st.cache_resource
def get_connection():
    # Connexion persistante en mémoire (plus rapide pour les démos) ou fichier
    conn = duckdb.connect(database=":memory:") 
    return conn

# Test git.