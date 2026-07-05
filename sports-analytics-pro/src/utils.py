# src/utils.py
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_sample_data(n=500):
    """
    Generate a synthetic dataset of athletes.
    """
    sports = ['Football', 'Basketball', 'Tennis', 'MMA', 'Cricket']
    data = {
        'Name': [fake.name() for _ in range(n)],
        'sport': np.random.choice(sports, n),
        'Age': np.random.randint(18, 40, n),
        'Height': np.random.normal(175, 10, n).astype(int),
        'Weight': np.random.normal(75, 15, n).astype(int),
        'performance_score': np.random.uniform(50, 100, n).round(2)
    }
    return pd.DataFrame(data)

def generate_mock_matches(n=5):
    """
    Return a list of mock live matches.
    """
    matches = []
    for _ in range(n):
        matches.append({
            'homeTeam': fake.company(),
            'awayTeam': fake.company(),
            'status': np.random.choice(['LIVE', 'FT', 'Scheduled'])
        })
    return matches