from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data(ttl=300, max_entries=4, show_spinner=False)
def load_data(path=None):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "clean" / "dataset.csv"
    return pd.read_csv(path)
