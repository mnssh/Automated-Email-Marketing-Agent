from sklearn.cluster import KMeans

def segment_users(df):
    k = KMeans(n_clusters=3, random_state=42)
    df['segment'] = k.fit_predict(df[['churn_risk','features_used']])
    df['segment_label'] = df['segment'].map({0:'New / Onboarding',1:'Engaged',2:'High Churn Risk'})
    return df
