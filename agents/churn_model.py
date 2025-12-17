import os, joblib
from sklearn.linear_model import LogisticRegression

def train_churn_model(df):
    os.makedirs('models', exist_ok=True)
    X = df[['logins_last_7d','features_used','last_login_days']]
    y = (df['inactive'] & df['low_usage']).astype(int)
    model = LogisticRegression()
    model.fit(X,y)
    df['churn_risk'] = model.predict_proba(X)[:,1]
    joblib.dump(model, 'models/churn_model.pkl')
    return df
