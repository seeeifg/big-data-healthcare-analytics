# Big Data Healthcare Analytics with MIMIC-III

[![Platform: Docker](https://img.shields.io/badge/Platform-Docker-2496ED?logo=docker&logoColor=white&style=flat-square)](https://www.docker.com/) 
[![Framework: Hadoop](https://img.shields.io/badge/Framework-Hadoop-66CC00?logo=apache&logoColor=white&style=flat-square)](https://hadoop.apache.org/)
[![Query Engine: Hive](https://img.shields.io/badge/Analytics-Hive-FDEE21?logo=apache-hive&logoColor=black&style=flat-square)](https://hive.apache.org/)
[![Compute: MapReduce](https://img.shields.io/badge/Compute-MapReduce-E34F26?style=flat-square)]
[![Dataset: MIMIC--III](https://img.shields.io/badge/Dataset-MIMIC--III-lightgrey?style=flat-square)](https://physionet.org/content/mimiciii-demo/1.4/)

This project implements a batch analytics pipeline on the **MIMIC-III Clinical Database (Demo v1.4)** using a fully containerized big data environment. It supports SQL-like querying via Hive and custom analytical jobs using MapReduce.

---

## Architecture Overview

| Component   | Description |
|------------|-------------|
| **Docker** | Multi-service container orchestration for Hadoop, Hive, and supporting services |
| **HDFS**   | Distributed storage system for scalable and fault-tolerant data storage |
| **Hive**   | SQL-like interface for querying structured MIMIC-III data |
| **MapReduce** | Java-based analytical processing engine |
| **MIMIC-III** | Public ICU dataset with demographics, diagnoses, mortality, and more |

---

## Project Structure

```
docker-hadoop-spark/
├── data/                   # Raw and cleaned MIMIC-III data (excluded from repo)
├── scripts/                # Python scripts to clean data and convert to Parquet
├── mapreduce/              # Mapper and reducer scripts for MapReduce job
├── docker-compose.yml      # Docker environment setup
├── Big Data Healthcare Analytics Project - Documentation.pdf
├── Project Brief.docx      # The original problem brief
└── README.md
```

---

## Setup Instructions
This section explains how to set up the project environment and run the full data pipeline — from cleaning raw CSVs to analyzing them in Hive and Hadoop MapReduce.

**1. Prerequisites**
* Git Bash (on Windows)

* Python 3.x installed with pip

* Docker + Docker Compose installed

* Git (to clone the repo and push changes)

* MIMIC-III Clinical Database Demo CSVs (placed in data/mimiciii/csv/)

**2. Install Python Dependencies**

pip install pandas pyarrow

**3. Start Hadoop and Hive containers**
```cd /c/Users/Seif/docker-hadoop-spark
docker-compose up -d
```
**4. Run the Data Cleaning Scripts**

* python scripts/convert_patients_to_parquet.py

* python scripts/convert_admissions_to_parquet.py

* python scripts/convert_icustays_to_parquet.py

* docker exec -it namenode bash

* hdfs dfs -mkdir -p /user/root/mimiciii/{patients,admissions,icustays}

* hdfs dfs -put /tmp/patients.parquet /user/root/mimiciii/patients/

* hdfs dfs -put /tmp/admissions.parquet /user/root/mimiciii/admissions/

* hdfs dfs -put /tmp/icustays.parquet /user/root/mimiciii/icustays/

**5. Create Hive Database and Tables**

* docker exec -it hive-server bash

* CREATE DATABASE IF NOT EXISTS mimiciii;
  
* USE mimiciii;

Then create the external tables.

**6. Run Hive Queries (Example)**

```sql
SELECT diagnosis, AVG(los)
FROM icustays
JOIN admissions USING (hadm_id)
GROUP BY diagnosis;
```

**7. Run MapReduce Job**

```bash
hadoop jar /root/avg.jar AverageAge \
  /user/root/clean_csv/PATIENTS_CLEAN \
  /user/root/output_avg
```
---

## Key Analytics Conducted

- **Average patient age** using MapReduce  
- **ICU readmission rates** via Hive  
- **Hospital and overall mortality** by demographic group  
- **ICU length of stay** by diagnosis  

---

## Data Model & Relationships

| Table       | Key Fields |
|-------------|------------|
| `patients`  | `subject_id`, `expire_flag` |
| `admissions` | `subject_id`, `hadm_id`, `diagnosis`, `hospital_expire_flag` |
| `icustays`  | `subject_id`, `hadm_id`, `los` (length of stay) |

**Joins Used:**
- `patients.subject_id = admissions.subject_id`  
- `admissions.hadm_id = icustays.hadm_id`  
- `patients.subject_id = icustays.subject_id`  

---

## Documentation

Refer to the file **Big Data Healthcare Analytics Project - Documentation.pdf** in this repository for a complete breakdown of the pipeline architecture, data flow, and technical decisions.

---

## Screenshots

**1. Average Length of Stay per Diagnosis (Hive)**  
![LOS](https://github.com/user-attachments/assets/e385ef81-965f-40c4-b417-5c934ba58b89)

**2. ICU Readmission Distribution (Hive)**  
![Readmissions](https://github.com/user-attachments/assets/c5b02b05-ee6f-4c69-a864-ddf34cde8476)

**3. Mortality by Ethnicity (Hive)**  
![Ethnicity Mortality](https://github.com/user-attachments/assets/e5274175-6a8e-4746-8432-a60d620e17be)

**4. Mortality by Gender (Hive)**  
![Gender Mortality](https://github.com/user-attachments/assets/df0b077c-0552-4c78-8005-1652355cabfa)

**5. Average Patient Age (MapReduce)**  
![Average Age](https://github.com/user-attachments/assets/8a79a939-e468-42ce-8ee6-8c2b64cd2097)

---

## Author

**GitHub:** [seeeifg](https://github.com/seeeifg)
