import pandas as pd
import os

# Input and Output paths
input_csv_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\ICUSTAYS.csv"
output_parquet_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\parquet\icustays.parquet"

# Load CSV
print("Reading ICUSTAYS.csv...")
df = pd.read_csv(input_csv_path)

# Drop completely empty rows
df_cleaned = df.dropna(how='all')

# Convert data types
df_cleaned['row_id'] = df_cleaned['row_id'].astype('int32')
df_cleaned['subject_id'] = df_cleaned['subject_id'].astype('int32')
df_cleaned['hadm_id'] = df_cleaned['hadm_id'].astype('Int64')  # nullable
df_cleaned['icustay_id'] = df_cleaned['icustay_id'].astype('int32')
df_cleaned['first_careunit'] = df_cleaned['first_careunit'].astype('string')
df_cleaned['last_careunit'] = df_cleaned['last_careunit'].astype('string')
df_cleaned['first_wardid'] = df_cleaned['first_wardid'].astype('Int64')
df_cleaned['last_wardid'] = df_cleaned['last_wardid'].astype('Int64')
df_cleaned['intime'] = pd.to_datetime(df_cleaned['intime'], errors='coerce')
df_cleaned['outtime'] = pd.to_datetime(df_cleaned['outtime'], errors='coerce')
df_cleaned['los'] = pd.to_numeric(df_cleaned['los'], errors='coerce')

# Ensure output directory exists
os.makedirs(os.path.dirname(output_parquet_path), exist_ok=True)

# Save to Parquet
print("Saving to Hive-compatible Parquet...")
df_cleaned.to_parquet(
    output_parquet_path,
    engine='pyarrow',
    index=False,
    coerce_timestamps='ms',
    use_deprecated_int96_timestamps=True  # Required for Hive compatibility
)

print("✅ Done! File saved at:")
print(output_parquet_path)