def track_behavior(df):
    df['inactive'] = df['last_login_days'] > 7
    df['low_usage'] = df['features_used'] <= 1
    return df
