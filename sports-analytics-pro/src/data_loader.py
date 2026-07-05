# src/data_loader.py
import pandas as pd
import streamlit as st
import os
from src.utils import generate_sample_data

@st.cache_data(ttl=3600)
def load_all_data(file_path: str = None) -> pd.DataFrame:
    # Get path from env if not passed
    if file_path is None:
        file_path = os.getenv("DATA_PATH", "")
    
    if file_path and os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = generate_sample_data(500)
    
    required = ['Name', 'sport', 'Age', 'Height', 'Weight', 'performance_score']
    if not all(col in df.columns for col in required):
        raise ValueError(f"Data missing required columns: {required}")
    
    return df