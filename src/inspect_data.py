import pandas as pd

DATA_PATH = "../data/"

def inspect_wind_data(file_name):
    df = pd.read_csv(DATA_PATH + file_name, sep=None, engine="python", encoding="latin1")

    print("=== BASIC INFO ===")
    print("Shape (rows, columns):", df.shape)

    print("\n=== COLUMN NAMES ===")
    print(df.columns.tolist())

    print("\n=== FIRST 5 ROWS ===")
    print(df.head())

    print("\n=== MISSING VALUES ===")
    print(df.isnull().sum())

if __name__ == "__main__":
    inspect_wind_data("wind_data_2017_18.txt")
    