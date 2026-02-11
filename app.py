import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Streamlit + DuckDB",
    layout="wide"
)

st.title("📊 Application d'analyse de données")
st.write("Bienvenue dans votre application Streamlit.")

uploaded_file = st.file_uploader("Téléverser un fichier CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Fichier chargé avec succès")
    st.dataframe(df.head())

