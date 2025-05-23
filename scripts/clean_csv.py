import pandas as pd
from datetime import datetime
import os

# Set input and output directories
input_dir = r'C:\Users\Seif\docker-hadoop-spark\data\mimiciii'
output_dir = r'C:\Users\Seif\docker-hadoop-spark\data\mimiciii\clean_csv'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def clean_icustays(file_path):
    df = pd.read_csv(file_path, na_values=[""])
    df = df.dropna(subset=['subject_id', 'hadm_id', 'icustay_id', 'intime', 'outtime'])
    df['intime'] = pd.to_datetime(df['intime'], errors='coerce')
    df['outtime'] = pd.to_datetime(df['outtime'], errors='coerce')
    df = df.dropna(subset=['intime', 'outtime'])
    df['los'] = pd.to_numeric(df['los'], errors='coerce')
    df = df.dropna(subset=['los'])
    df['subject_id'] = df['subject_id'].astype(int)
    df['hadm_id'] = df['hadm_id'].astype(int)
    df['icustay_id'] = df['icustay_id'].astype(int)
    df['first_wardid'] = pd.to_numeric(df['first_wardid'], errors='coerce').astype('Int64')
    df['last_wardid'] = pd.to_numeric(df['last_wardid'], errors='coerce').astype('Int64')
    return df

def clean_patients(file_path):
    df = pd.read_csv(file_path, na_values=[""])
    df = df.dropna(subset=['subject_id', 'gender', 'dob'])
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
    for col in ['dod', 'dod_hosp', 'dod_ssn']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df = df.dropna(subset=['dob'])
    df['subject_id'] = df['subject_id'].astype(int)
    df['expire_flag'] = df['expire_flag'].astype(int)
    return df

def clean_admissions(file_path):
    df = pd.read_csv(file_path, na_values=[""])
    df = df.dropna(subset=['subject_id', 'hadm_id', 'admittime', 'dischtime'])
    df['admittime'] = pd.to_datetime(df['admittime'], errors='coerce')
    df['dischtime'] = pd.to_datetime(df['dischtime'], errors='coerce')
    df['deathtime'] = pd.to_datetime(df['deathtime'], errors='coerce')
    df['edregtime'] = pd.to_datetime(df['edregtime'], errors='coerce')
    df['edouttime'] = pd.to_datetime(df['edouttime'], errors='coerce')
    df = df.dropna(subset=['admittime', 'dischtime'])
    df['subject_id'] = df['subject_id'].astype(int)
    df['hadm_id'] = df['hadm_id'].astype(int)
    df['hospital_expire_flag'] = df['hospital_expire_flag'].astype(int)
    df['has_chartevents_data'] = df['has_chartevents_data'].astype(int)
    text_cols = ['admission_type', 'admission_location', 'discharge_location', 
                 'insurance', 'language', 'religion', 'marital_status', 'ethnicity', 'diagnosis']
    for col in text_cols:
        df[col] = df[col].str.strip()
    return df

# Build full paths for each file
icustays_path = os.path.join(input_dir, 'ICUSTAYS.csv')
patients_path = os.path.join(input_dir, 'PATIENTS.csv')
admissions_path = os.path.join(input_dir, 'ADMISSIONS.csv')

# Clean each file
icustays_clean = clean_icustays(icustays_path)
patients_clean = clean_patients(patients_path)
admissions_clean = clean_admissions(admissions_path)

# Save cleaned files to output directory
icustays_clean.to_csv(os.path.join(output_dir, 'ICUSTAYS_clean.csv'), index=False)
patients_clean.to_csv(os.path.join(output_dir, 'PATIENTS_clean.csv'), index=False)
admissions_clean.to_csv(os.path.join(output_dir, 'ADMISSIONS_clean.csv'), index=False)

print("Cleaning complete. Cleaned files saved in:")
print(output_dir)
