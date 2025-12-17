import numpy as np

def track_performance(df):
    df['opened'] = np.random.choice([0,1], len(df))
    df['clicked'] = np.random.choice([0,1], len(df))
    return df['opened'].mean(), df['clicked'].mean(), df
