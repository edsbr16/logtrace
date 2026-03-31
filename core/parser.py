import pandas as pd

def load_log(filepath):
    df = pd.read_csv(filepath)
    return df

def clean_log(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.dropna(subset=['timestamp', 'ip_address', 'username', 'event_type'])
    return df

if __name__ == "__main__":
    df = load_log("sample_data/brute_force.csv")
    df = clean_log(df)
    print(df)
    print(df.dtypes)
    