import pandas as pd
import os
from datetime import datetime
import numpy as np

# Set paths
csv_dir = 'data/mimiciii'
parquet_dir = 'data/parquet'
os.makedirs(parquet_dir, exist_ok=True)

# Custom datetime parser with better error handling
def parse_datetime(dt_str):
    if pd.isna(dt_str):
        return pd.NaT
    try:
        # Try the most common format first
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            # Try without seconds if that fails
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                # Try date only
                return datetime.strptime(dt_str, '%Y-%m-%d')
            except ValueError:
                return pd.NaT

# Convert specified columns to datetime with better handling
def safe_datetime(df, date_cols):
    for col in date_cols:
        if col in df.columns:
            # First try with pandas to_datetime
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Check if we have any remaining invalid dates
            if df[col].isna().any():
                # Fall back to custom parser for problematic dates
                df[col] = df[col].astype(str).apply(parse_datetime)
                
    return df

# Function to safely convert columns to integer, handling NA values
def safe_int(df, col_name):
    if col_name in df.columns:
        # First convert to float to handle NA values, then to nullable Int32
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce').astype('float32')
        # Convert to nullable integer type if no decimals
        if (df[col_name] % 1 == 0).all():
            df[col_name] = pd.to_numeric(df[col_name], downcast='integer')
    return df

# Function to clean and optimize each dataframe
def clean_file(file_name):
    path = os.path.join(csv_dir, file_name)
    print(f"Reading {path}...")
    
    # Read CSV with appropriate dtype hints to reduce memory usage
    dtype_hints = {
        'row_id': 'int32',
        'subject_id': 'int32',
        'hadm_id': 'float32',  # Changed to float to handle NA values
        'icustay_id': 'float32',
        'itemid': 'int32',
        'value': 'str',
        'valuenum': 'float32',
        'cgid': 'float32'
    }
    
    # Read CSV with chunks if large (for memory efficiency)
    try:
        chunks = pd.read_csv(path, chunksize=100000, dtype=dtype_hints, low_memory=False)
        df = pd.concat(chunks, ignore_index=True)
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        # Fallback to regular read if chunking fails
        df = pd.read_csv(path, dtype=dtype_hints, low_memory=False)
    
    # Basic cleaning
    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)
    
    # Trim whitespace from string columns
    str_cols = df.select_dtypes(['object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
    
    # Convert empty strings to NaN
    df.replace('', np.nan, inplace=True)
    
    # File-specific processing
    if file_name == 'PATIENTS.csv':
        df = safe_datetime(df, ['dob', 'dod', 'dod_hosp', 'dod_ssn'])
        # Ensure subject_id is correct
        df['subject_id'] = df['subject_id'].astype('int32')
        
    elif file_name == 'ADMISSIONS.csv':
        df = safe_datetime(df, [
            'admittime', 'dischtime', 'deathtime',
            'edregtime', 'edouttime'
        ])
        # Convert IDs to appropriate types
        df['subject_id'] = df['subject_id'].astype('int32')
        df['hadm_id'] = df['hadm_id'].astype('int32')
        
    elif file_name == 'ICUSTAYS.csv':
        df = safe_datetime(df, ['intime', 'outtime'])
        df['subject_id'] = df['subject_id'].astype('int32')
        df['hadm_id'] = df['hadm_id'].astype('int32')
        df['icustay_id'] = df['icustay_id'].astype('int32')
        
    elif file_name == 'LABEVENTS.csv':
        df = safe_datetime(df, ['charttime'])
        df['subject_id'] = df['subject_id'].astype('int32')
        # Handle hadm_id which might contain NA values
        df = safe_int(df, 'hadm_id')
        df['itemid'] = df['itemid'].astype('int32')
        if 'valuenum' in df.columns:
            df['valuenum'] = df['valuenum'].astype('float32')
        
    elif file_name == 'D_LABITEMS.csv':
        df['itemid'] = df['itemid'].astype('int32')
        # No datetime conversion needed
        
    # Downcast numeric columns to save space
    for col in df.select_dtypes(['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

# Files to process
files = [
    'PATIENTS.csv',
    'ADMISSIONS.csv',
    'ICUSTAYS.csv',
    'LABEVENTS.csv',
    'D_LABITEMS.csv'
]

# Clean and convert each to Parquet
for file in files:
    print(f"\nProcessing {file}...")
    start_time = datetime.now()
    
    try:
        df = clean_file(file)
        
        # Print some info about the processed data
        print(f"Processed {len(df)} rows")
        print("Data types:")
        print(df.dtypes)
        
        # Check date columns
        date_cols = df.select_dtypes(include=['datetime64[ns]']).columns
        for col in date_cols:
            print(f"\nDate column '{col}' info:")
            print(f"Range: {df[col].min()} to {df[col].max()}")
            print(f"Null values: {df[col].isna().sum()}")
        
        parquet_path = os.path.join(parquet_dir, file.replace('.csv', '.parquet'))
        
        # Write with pyarrow to preserve datatypes and enable compression
        df.to_parquet(
            parquet_path,
            engine='pyarrow',
            compression='snappy',  # Good balance of speed and compression
            index=False
        )
        
        print(f"Written to {parquet_path}")
        print(f"Processing time: {datetime.now() - start_time}")
    
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")
        continue

print("\nAll files processed successfully!")