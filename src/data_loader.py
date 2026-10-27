from pathlib import Path

import pandas as pd


# TODO: adicionar @st.cache_data (import streamlit as st) para evitar reler o CSV a cada interação
def load_data(path=None):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "clean" / "dataset.csv"
    return pd.read_csv(path)
