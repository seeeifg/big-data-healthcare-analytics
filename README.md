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
├── docker-compose.yml      # Docker environment setup
├── Documentation.pdf       # In-depth explanation of pipeline architecture
├── Project Brief.docx      # The original problem brief
└── README.md
```

---

## Setup Instructions

**1. Start Hadoop and Hive containers**
```bash
docker-compose up -d
```

**2. Create directories and upload cleaned data to HDFS**
```bash
hdfs dfs -mkdir -p /user/root/clean_csv
hdfs dfs -put ./clean_csv/PATIENTS_CLEAN /user/root/clean_csv/
```

**3. Run MapReduce Job**
```bash
hadoop jar /root/avg.jar AverageAge \
  /user/root/clean_csv/PATIENTS_CLEAN \
  /user/root/output_avg
```

**4. Run Hive Queries (Example)**
```sql
SELECT diagnosis, AVG(los)
FROM icustays
JOIN admissions USING (hadm_id)
GROUP BY diagnosis;
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

For full architectural and implementation details, refer to the [**Documentation.pdf**](./Documentation.pdf) in this repository.

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
