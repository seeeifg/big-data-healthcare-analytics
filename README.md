# Big Data Healthcare Analytics with MIMIC-III

[![Platform](https://img.shields.io/badge/Platform-Docker-2496ED?logo=docker&logoColor=white&style=flat-square)](https://www.docker.com/)
[![Framework](https://img.shields.io/badge/Framework-Hadoop-66CC00?logo=apache-hadoop&logoColor=white&style=flat-square)](https://hadoop.apache.org/)
[![Query Engine](https://img.shields.io/badge/Query_Engine-Hive-FDEE21?logo=apache-hive&logoColor=black&style=flat-square)](https://hive.apache.org/)
[![Compute](https://img.shields.io/badge/Compute-MapReduce-E44D26?style=flat-square)](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/)
[![Dataset](https://img.shields.io/badge/Dataset-MIMIC--III-999999?style=flat-square)](https://physionet.org/content/mimiciii-demo/1.4/)

This project builds a batch analytics pipeline based on the MIMIC-III Clinical Database (Demo v1.4) using a Docker-based big data environment. It supports structured querying via Hive and parallel analytics using MapReduce.

---

## Project Scope

This project focuses on the batch processing and analytics of ICU patient data from the MIMIC-III Clinical Database using a Dockerized big data stack. It is intended for educational and research purposes to demonstrate the use of Hadoop, Hive, and MapReduce in healthcare analytics.

**In Scope**

* Environment Setup with Docker: Deploy Hadoop and Hive using Docker containers for reproducibility and isolation.

* Data Ingestion: Convert raw CSV files to Parquet format using Python, then load them into HDFS.

* Structured Querying with Hive: Perform analytical queries such as ICU readmission rates and mortality breakdowns.

* MapReduce Analytics: Implement a custom MapReduce job in Java to calculate the average patient age.

* Visualization: Present key analytics via screenshots and query outputs.

 ---

## Architecture Overview

| Component     | Description |
|---------------|-------------|
| **Docker**    | Container orchestration for Hadoop, Hive, and supporting services |
| **HDFS**      | Distributed storage system |
| **Hive**      | SQL-like querying interface |
| **MapReduce** | Java-based batch analytics engine |
| **MIMIC-III** | Public ICU dataset for healthcare analytics |


![healthcare_arch](https://github.com/user-attachments/assets/65e5774a-642d-47cb-9885-ff121379717d)

---

## Project Directory Structure

```
docker-hadoop-spark/
├── data/                         # Raw and cleaned MIMIC-III files
├── scripts/                      # Python scripts for cleaning and Parquet conversion
├── mapreduce/                    # Java MapReduce source and compiled JARs
├── docker-compose.yml            # Docker environment config
├── Big Data Healthcare Analytics Project - Documentation.pdf
├── Project Brief.docx
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Git Bash (Windows)
- Python 3.x with pip
- Docker and Docker Compose
- Git CLI
- MIMIC-III Demo CSV files in `data/mimiciii/csv/`

### Step 1: Install Python Dependencies

```bash
pip install pandas pyarrow
```

### Step 2: Start Hadoop + Hive Containers

```bash
cd /c/Users/Seif/docker-hadoop-spark
docker-compose up -d
```

### Step 3: Convert CSVs to Parquet and Load into HDFS

```bash
python scripts/convert_patients_to_parquet.py
python scripts/convert_admissions_to_parquet.py
python scripts/convert_icustays_to_parquet.py

docker exec -it namenode bash

hdfs dfs -mkdir -p /user/root/mimiciii/{patients,admissions,icustays}
hdfs dfs -put /tmp/patients.parquet /user/root/mimiciii/patients/
hdfs dfs -put /tmp/admissions.parquet /user/root/mimiciii/admissions/
hdfs dfs -put /tmp/icustays.parquet /user/root/mimiciii/icustays/
```

### Step 4: Create Hive Tables

```bash
docker exec -it hive-server bash
```

In Hive CLI:

```sql
CREATE DATABASE IF NOT EXISTS mimiciii;
USE mimiciii;

CREATE EXTERNAL TABLE patients (
  subject_id INT,
  gender STRING,
  dob TIMESTAMP,
  dod TIMESTAMP,
  expire_flag INT
)
STORED AS PARQUET
LOCATION '/user/root/mimiciii/patients';

-- Repeat for admissions and icustays
```

---

## Example Hive Query

```sql
SELECT a.diagnosis, ROUND(AVG(i.los), 2) AS avg_los
FROM icustays i
JOIN admissions a ON i.hadm_id = a.hadm_id
GROUP BY a.diagnosis
ORDER BY avg_los DESC;
```

---

## Run MapReduce Job

```bash
hadoop jar /root/avg.jar AverageAge \
  /user/root/clean_csv/PATIENTS_CLEAN \
  /user/root/output_avg
```

---

## Key Analytics Conducted

| Analysis                             | Tool       |
|--------------------------------------|------------|
| Average Patient Age                  | MapReduce  |
| ICU Readmission Rate                 | Hive       |
| Mortality by Gender and Ethnicity    | Hive       |
| ICU Length of Stay by Diagnosis      | Hive       |

---

## Data Model & Relationships

| Table       | Key Fields                                 |
|-------------|---------------------------------------------|
| `patients`  | `subject_id`, `expire_flag`                 |
| `admissions`| `subject_id`, `hadm_id`, `diagnosis`        |
| `icustays`  | `subject_id`, `hadm_id`, `los`              |

**Relationships**:

- `patients.subject_id = admissions.subject_id`  
- `admissions.hadm_id = icustays.hadm_id`  
- `patients.subject_id = icustays.subject_id`

---

## Documentation

Refer to [Big Data Healthcare Analytics Project - Documentation.pdf](https://github.com/seeeifg/mimiciii-big-data-healthcare-analytics/blob/master/Big%20Data%20Healthcare%20Analytics%20Project%20-%20Documentation.pdf) for detailed technical architecture, schema design, and analysis overview.

---

## Screenshots

<p align="center"> <strong>1. Average Length of Stay per Diagnosis (Hive)</strong><br> <img src="https://github.com/user-attachments/assets/e385ef81-965f-40c4-b417-5c934ba58b89" alt="LOS" width="600"/> </p> <p align="center"> <strong>2. ICU Readmission Distribution (Hive)</strong><br> <img src="https://github.com/user-attachments/assets/c5b02b05-ee6f-4c69-a864-ddf34cde8476" alt="Readmissions" width="600"/> </p> <p align="center"> <strong>3. Mortality by Ethnicity (Hive)</strong><br> <img src="https://github.com/user-attachments/assets/e5274175-6a8e-4746-8432-a60d620e17be" alt="Ethnicity Mortality" width="600"/> </p> <p align="center"> <strong>4. Mortality by Gender (Hive)</strong><br> <img src="https://github.com/user-attachments/assets/df0b077c-0552-4c78-8005-1652355cabfa" alt="Gender Mortality" width="600"/> </p> <p align="center"> <strong>5. Average Patient Age (MapReduce)</strong><br> <img src="https://github.com/user-attachments/assets/8a79a939-e468-42ce-8ee6-8c2b64cd2097" alt="Average Age" width="600"/> </p>

---

## Sources

**Source Environment:** https://github.com/Marcel-Jan/docker-hadoop-spark

**MIMIC-III Dataset:** https://physionet.org/content/mimiciii-demo/1.4

--- 

## Author

**GitHub:** [seeeifg](https://github.com/seeeifg)
