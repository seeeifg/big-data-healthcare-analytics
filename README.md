# Big Data Healthcare Analytics with MIMIC-III

[![Platform: Docker](https://img.shields.io/badge/Platform-Docker-2496ED?logo=docker&logoColor=white&style=flat-square)](https://www.docker.com/) 
[![Framework: Hadoop](https://img.shields.io/badge/Framework-Hadoop-66CC00?logo=apache&logoColor=white&style=flat-square)](https://hadoop.apache.org/)
[![Query Engine: Hive](https://img.shields.io/badge/Analytics-Hive-FDEE21?logo=apache-hive&logoColor=black&style=flat-square)](https://hive.apache.org/)
[![Compute: MapReduce](https://img.shields.io/badge/Compute-MapReduce-E34F26?style=flat-square)]
[![Dataset: MIMIC--III](https://img.shields.io/badge/Dataset-MIMIC--III-lightgrey?style=flat-square)](https://physionet.org/content/mimiciii-demo/1.4/)

This project implements a batch analytics pipeline on the **MIMIC-III Clinical Database (Demo v1.4)** using a fully containerized big data environment. It supports SQL-style queries through Hive and custom analytical jobs using MapReduce in Java.

---

## 🔧 Architecture Overview

| Component   | Description |
|------------|-------------|
| **Docker** | Orchestrates Hadoop, Hive, and supporting services in containers |
| **HDFS**   | Distributed file system for scalable storage |
| **Hive**   | SQL interface for structured query processing |
| **MapReduce** | Java-based engine for custom analytics |
| **MIMIC-III** | Public ICU dataset with patient-level clinical records |

---

## 📁 Project Structure

```
docker-hadoop-spark/
├── data/                   # Raw and cleaned MIMIC-III data (excluded from repo)
├── scripts/                # Python scripts to clean data and convert to Parquet
├── mapreduce/              # Java mapper and reducer scripts
├── docker-compose.yml      # Containerized Hadoop-Hive setup
├── Big Data Healthcare Analytics Project - Documentation.pdf
├── Project Brief.docx
└── README.md
```

---

## 🛠️ Setup Instructions

This guide walks through setting up the environment, cleaning data, uploading it to HDFS, and analyzing it using Hive and MapReduce.

### 1. Prerequisites

- Git Bash (for Windows)
- Python 3.x with pip
- Docker + Docker Compose
- Git
- MIMIC-III Demo CSVs in: `data/mimiciii/csv/`

---

### 2. Install Python Dependencies

```bash
pip install pandas pyarrow
```

---

### 3. Start Docker Containers

```bash
cd /c/Users/Seif/docker-hadoop-spark
docker-compose up -d
```

---

### 4. Run Data Cleaning Scripts

```bash
python scripts/convert_patients_to_parquet.py
python scripts/convert_admissions_to_parquet.py
python scripts/convert_icustays_to_parquet.py
```

Then inside the Hadoop container:

```bash
docker exec -it namenode bash
hdfs dfs -mkdir -p /user/root/mimiciii/{patients,admissions,icustays}
hdfs dfs -put /tmp/patients.parquet /user/root/mimiciii/patients/
hdfs dfs -put /tmp/admissions.parquet /user/root/mimiciii/admissions/
hdfs dfs -put /tmp/icustays.parquet /user/root/mimiciii/icustays/
```

---

### 5. Set Up Hive Schema

Inside the Hive container:

```bash
docker exec -it hive-server bash
```

In Hive shell:

```sql
CREATE DATABASE IF NOT EXISTS mimiciii;
USE mimiciii;
-- Then create external tables based on Parquet format
```

---

### 6. Run Hive Queries (Example)

```sql
SELECT diagnosis, AVG(los)
FROM icustays
JOIN admissions USING (hadm_id)
GROUP BY diagnosis;
```

---

### 7. Run MapReduce Job

```bash
hadoop jar /root/avg.jar AverageAge \
  /user/root/clean_csv/PATIENTS_CLEAN \
  /user/root/output_avg
```

---

## 📊 Key Analytics

- Average patient age — MapReduce  
- ICU readmission rates — Hive  
- Mortality breakdowns — Hive  
- Length of stay by diagnosis — Hive  

---

## 🧬 Data Model

| Table       | Key Fields |
|-------------|------------|
| `patients`  | `subject_id`, `expire_flag` |
| `admissions` | `subject_id`, `hadm_id`, `diagnosis`, `hospital_expire_flag` |
| `icustays`  | `subject_id`, `hadm_id`, `los` |

**Joins Used:**

- `patients.subject_id = admissions.subject_id`  
- `admissions.hadm_id = icustays.hadm_id`  
- `patients.subject_id = icustays.subject_id`  

---

## 📄 Documentation

See **Big Data Healthcare Analytics Project - Documentation.pdf** for the full technical breakdown, data pipeline, architecture, and justification of tools used.

---

## 🖼️ Screenshots

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

## 👤 Author

**GitHub:** [seeeifg](https://github.com/seeeifg)
