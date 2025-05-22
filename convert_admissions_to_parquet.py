import pandas as pd
import os

# Input and Output paths
input_csv_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\ADMISSIONS.csv"
output_parquet_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\parquet\admissions.parquet"

# Load CSV
print("Reading ADMISSIONS.csv...")
df = pd.read_csv(input_csv_path)

# Drop completely empty rows
df_cleaned = df.dropna(how='all')

# Convert data types
df_cleaned['row_id'] = df_cleaned['row_id'].astype('int32')
df_cleaned['subject_id'] = df_cleaned['subject_id'].astype('int32')
df_cleaned['hadm_id'] = df_cleaned['hadm_id'].astype('int32')
df_cleaned['admittime'] = pd.to_datetime(df_cleaned['admittime'], errors='coerce')
df_cleaned['dischtime'] = pd.to_datetime(df_cleaned['dischtime'], errors='coerce')
df_cleaned['deathtime'] = pd.to_datetime(df_cleaned['deathtime'], errors='coerce')
df_cleaned['admission_type'] = df_cleaned['admission_type'].astype('string')
df_cleaned['admission_location'] = df_cleaned['admission_location'].astype('string')
df_cleaned['discharge_location'] = df_cleaned['discharge_location'].astype('string')
df_cleaned['insurance'] = df_cleaned['insurance'].astype('string')
df_cleaned['language'] = df_cleaned['language'].astype('string')
df_cleaned['religion'] = df_cleaned['religion'].astype('string')
df_cleaned['marital_status'] = df_cleaned['marital_status'].astype('string')
df_cleaned['ethnicity'] = df_cleaned['ethnicity'].astype('string')
df_cleaned['edregtime'] = pd.to_datetime(df_cleaned['edregtime'], errors='coerce')
df_cleaned['edouttime'] = pd.to_datetime(df_cleaned['edouttime'], errors='coerce')
df_cleaned['diagnosis'] = df_cleaned['diagnosis'].astype('string')
df_cleaned['hospital_expire_flag'] = df_cleaned['hospital_expire_flag'].astype('int8')
df_cleaned['has_chartevents_data'] = df_cleaned['has_chartevents_data'].astype('int8')

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