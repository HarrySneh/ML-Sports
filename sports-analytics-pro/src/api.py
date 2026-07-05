# src/api.py
import requests
import streamlit as st
import os
from src.utils import generate_mock_matches

@st.cache_data(ttl=300)
def get_live_matches():
    url = os.getenv("LIVE_MATCHES_API_URL")
    api_key = os.getenv("API_KEY")
    
    if not url or not api_key:
        return generate_mock_matches(10)
    
    try:
        headers = {"X-Auth-Token": api_key}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        matches = data.get('matches', [])
        results = []
        for m in matches[:10]:
            results.append({
                'homeTeam': m.get('homeTeam', {}).get('name', 'Unknown'),
                'awayTeam': m.get('awayTeam', {}).get('name', 'Unknown'),
                'status': m.get('status', 'Unknown')
            })
        return results
    except Exception as e:
        st.warning(f"Could not fetch live data: {e}. Showing mock data.")
        return generate_mock_matches(10)