# src/model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import streamlit as st

@st.cache_resource
def train_model(df: pd.DataFrame):
    """
    Train a binary classifier (high vs low performance) using Age, Height, Weight.
    Returns the model and the fitted scaler.
    """
    X = df[['Age', 'Height', 'Weight']]
    # Create binary target: 1 if performance_score > median, else 0
    y = (df['performance_score'] > df['performance_score'].median()).astype(int)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler