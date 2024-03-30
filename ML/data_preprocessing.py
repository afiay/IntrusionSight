# data_preprocessing.py
import sqlite3
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

def calculate_time_deltas(df):
    df['timestamp'] = pd.to_datetime(
        df['timestamp'], format="%Y-%m-%d %H:%M:%S.%f")
    df = df.sort_values(by='timestamp')
    df['time_delta'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    return df

def calculate_moving_averages(df, window_size=10):
    df['avg_time_delta'] = df['time_delta'].rolling(
        window=window_size, min_periods=1).mean()
    df['avg_requests'] = df['requests'].rolling(
        window=window_size, min_periods=1).mean()
    return df

def load_data(database_path='../users.db', table_name='network_traffic'):
    conn = sqlite3.connect(database_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def preprocess_data(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        df.replace('N/A', np.nan).infer_objects(copy=False)

    df.ffill(inplace=True)
    df.drop(['src_ip', 'dst_ip', 'timestamp'], axis=1, inplace=True)

    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    numerical_cols = df.select_dtypes(include=[np.number]).columns
    df[numerical_cols] = StandardScaler().fit_transform(df[numerical_cols])

    return df

def get_features_labels(df, label_col='label'):
    X = df.drop(label_col, axis=1)
    y = df[label_col]
    return train_test_split(X, y, test_size=0.2, random_state=42)

if __name__ == '__main__':
    df = load_data()
    df = calculate_time_deltas(df)
    df = calculate_moving_averages(df)
    df_processed = preprocess_data(df)
    X_train, X_test, y_train, y_test = get_features_labels(df_processed)
