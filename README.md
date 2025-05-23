# Big Data Healthcare Analytics with MIMIC-III
This project implements a big data pipeline for batch analytics on the MIMIC-III Clinical Database. It uses Docker to run a Hadoop + Hive environment, and applies MapReduce for analytical tasks on ICU patient data.

**Architecture**
Docker: Containerized multi-service setup
Hadoop + HDFS: Distributed data storage
Hive: SQL-based querying for batch analytics
MapReduce: Custom Java program to compute patient age statistics
MIMIC-III (Demo v1.4): Clinical dataset for ICU patients

**Project Structure**
graphql
Copy
Edit
docker-hadoop-spark/
├── data/                   # Raw and cleaned MIMIC-III data (excluded from repo)
├── scripts/                # Python scripts used to clean and convert to Parquet
├── docker-compose.yml      # Environment setup
├── Documentation.pdf       # In-depth breakdown of the project's workflow
├── Project Brief.docx      # The brief based on which the project was conducted
├── README.md

## Setup Instructions

**Start the cluster:**
docker-compose up -d

**Copy data into HDFS:**
hdfs dfs -mkdir -p /user/root/clean_csv
hdfs dfs -put ./clean_csv/PATIENTS_CLEAN /user/root/clean_csv/

**Run MapReduce job:**
hadoop jar /root/avg.jar AverageAge \
  /user/root/clean_csv/PATIENTS_CLEAN \
  /user/root/output_avg
  
**Query with Hive:**
Example: Average ICU length of stay by diagnosis

## Examples of Key Analytics
Average patient age (MapReduce)
ICU readmissions (Hive)
Mortality rates (Hive)

## Data Model

**Relationships**
patients.subject_id = admissions.subject_id
admissions.hadm_id = icustays.hadm_id
patients.subject_id = icustays.subject_id

**Measures**
los — ICU length of stay
hospital_expire_flag — hospital mortality
expire_flag — overall mortality
diagnosis — admission diagnosis

## Documentation
Read the Big Data Healthcare Analytics Project - Documentation file for an in-depth breakdown

## Screenshots

**1. Average Length of Stay per Diagnosis - Hive Query**

![image](https://github.com/user-attachments/assets/e385ef81-965f-40c4-b417-5c934ba58b89)

**2. Distribution of ICU Readmissions - Hive Query**

![image](https://github.com/user-attachments/assets/c5b02b05-ee6f-4c69-a864-ddf34cde8476)

**3. Mortality Rates by Demographic Groups (Ethnicity) - Hive Query**

![image](https://github.com/user-attachments/assets/e5274175-6a8e-4746-8432-a60d620e17be)

**4. Mortality Rates by Gender - Hive Query**

![image](https://github.com/user-attachments/assets/df0b077c-0552-4c78-8005-1652355cabfa)

**5. Average Age of Patients - Map Reduce Task**

![image](https://github.com/user-attachments/assets/8a79a939-e468-42ce-8ee6-8c2b64cd2097)

**Author:** seeeifg
**GitHub:** https://github.com/seeeifg
