import pandas as pd
import os

# Input and Output paths
input_csv_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\PATIENTS.csv"
output_parquet_path = r"C:\Users\Seif\docker-hadoop-spark\data\mimiciii\parquet\patients.parquet"

# Load CSV
print("Reading PATIENTS.csv...")
df = pd.read_csv(input_csv_path)
df.columns = df.columns.str.strip().str.upper()

# Drop empty rows
df_cleaned = df.dropna(how='all')

# Convert data types (Hive-friendly)
df_cleaned['SUBJECT_ID'] = df_cleaned['SUBJECT_ID'].astype('int32')
df_cleaned['GENDER'] = df_cleaned['GENDER'].astype('string')
df_cleaned['DOB'] = pd.to_datetime(df_cleaned['DOB'], errors='coerce')
df_cleaned['DOD'] = pd.to_datetime(df_cleaned['DOD'], errors='coerce')
df_cleaned['DOD_HOSP'] = pd.to_datetime(df_cleaned['DOD_HOSP'], errors='coerce')
df_cleaned['DOD_SSN'] = pd.to_datetime(df_cleaned['DOD_SSN'], errors='coerce')
df_cleaned['EXPIRE_FLAG'] = df_cleaned['EXPIRE_FLAG'].astype('int8')

# Ensure output folder exists
os.makedirs(os.path.dirname(output_parquet_path), exist_ok=True)

# Save to Parquet with Hive-compatible timestamp format
print("Saving to Hive-compatible Parquet...")
df_cleaned.to_parquet(
    output_parquet_path,
    engine='pyarrow',
    index=False,
    coerce_timestamps='ms',
    use_deprecated_int96_timestamps=True  # Critical for Hive
)

print("✅ Done! File saved at:")
print(output_parquet_path)
