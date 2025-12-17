import os, joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier

def optimize_send_time(df):
    os.makedirs('models', exist_ok=True)
    X = df[['logins_last_7d','features_used','last_login_days']]
    y = np.random.choice([9,12,18], size=len(df))
    model = RandomForestClassifier()
    model.fit(X,y)
    joblib.dump(model,'models/send_time_model.pkl')
    df['best_send_hour'] = model.predict(X)
    return df
