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
├── Big Data Healthcare Analytics Project - Documentation.pdf
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

1. System Architecture Diagram
mermaidgraph TB
    subgraph "Data Sources"
        A[MIMIC-III Clinical Database]
        A1[PATIENTS.csv]
        A2[ADMISSIONS.csv] 
        A3[ICUSTAYS.csv]
        A --> A1
        A --> A2
        A --> A3
    end

    subgraph "Docker Container Environment"
        subgraph "Hadoop Ecosystem"
            B[Hadoop HDFS]
            C[Hadoop MapReduce]
            D[Hive Metastore]
            E[Hive Server]
        end
        
        subgraph "Processing Layer"
            F[Apache Hive]
            G[HiveQL Queries]
        end
    end

    subgraph "Analytics Outputs"
        H[Length-of-Stay Analysis]
        I[Readmission Analysis]
        J[Mortality Rate Analysis]
        K[Batch Reports]
    end

    A1 --> B
    A2 --> B
    A3 --> B
    B --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    H --> K
    I --> K
    J --> K

    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style F fill:#e8f5e8
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#fff3e0
2. Data Flow Architecture
mermaidflowchart LR
    subgraph "Ingestion"
        A[Raw CSV Files]
        B[Data Validation]
        C[Format Conversion]
    end
    
    subgraph "Storage"
        D[HDFS Cluster]
        E[Parquet Format]
        F[Distributed Blocks]
    end
    
    subgraph "Processing"
        G[Hive Tables]
        H[Schema Definition]
        I[Query Execution]
    end
    
    subgraph "Analytics"
        J[LOS Prediction]
        K[Readmission Risk]
        L[Mortality Analysis]
    end
    
    subgraph "Output"
        M[Batch Results]
        N[Reports]
        O[Visualizations]
    end

    A --> B --> C
    C --> D --> E --> F
    F --> G --> H --> I
    I --> J
    I --> K
    I --> L
    J --> M --> N --> O
    K --> M
    L --> M

    style A fill:#ffebee
    style D fill:#e3f2fd
    style G fill:#e8f5e8
    style J fill:#fff8e1
    style K fill:#fff8e1
    style L fill:#fff8e1
3. Docker Container Architecture
mermaidgraph TB
    subgraph "Docker Host"
        subgraph "Hadoop Cluster"
            A[NameNode Container]
            B[DataNode Container 1]
            C[DataNode Container 2]
            D[ResourceManager]
            E[NodeManager]
        end
        
        subgraph "Hive Services"
            F[Hive Metastore]
            G[Hive Server2]
            H[MySQL Database]
        end
        
        subgraph "Infrastructure"
            I[Docker Network]
            J[HDFS Volume]
            K[Hive Warehouse]
        end
    end

    A -.-> I
    B -.-> I
    C -.-> I
    D -.-> I
    E -.-> I
    F -.-> I
    G -.-> I

    A --> J
    B --> J
    C --> J
    F --> K
    G --> K
    F --> H

    style A fill:#2196f3,color:#fff
    style B fill:#4caf50,color:#fff
    style C fill:#4caf50,color:#fff
    style F fill:#ff9800,color:#fff
    style G fill:#ff9800,color:#fff
4. Data Model Relationships
mermaiderDiagram
    PATIENTS {
        int SUBJECT_ID PK
        varchar GENDER
        timestamp DOB
        timestamp DOD
        int EXPIRE_FLAG
    }
    
    ADMISSIONS {
        int SUBJECT_ID FK
        int HADM_ID PK
        timestamp ADMITTIME
        timestamp DISCHTIME
        varchar ADMISSION_TYPE
        varchar DISCHARGE_LOCATION
        varchar ETHNICITY
        text DIAGNOSIS
        int HOSPITAL_EXPIRE_FLAG
    }
    
    ICUSTAYS {
        int SUBJECT_ID FK
        int HADM_ID FK
        int ICUSTAY_ID PK
        varchar FIRST_CAREUNIT
        timestamp INTIME
        timestamp OUTTIME
        numeric LOS
    }

    PATIENTS ||--o{ ADMISSIONS : "has multiple"
    ADMISSIONS ||--o{ ICUSTAYS : "includes"
5. Technology Stack
mermaidgraph TB
    subgraph "Infrastructure"
        A[Docker Compose]
        B[Linux Containers]
    end
    
    subgraph "Storage"
        C[Hadoop HDFS]
        D[Distributed Storage]
    end
    
    subgraph "Processing"
        F[Apache Hive]
        G[HiveQL Engine]
    end
    
    subgraph "Data"
        I[MIMIC-III Dataset]
        J[Parquet Files]
    end
    
    subgraph "Analytics"
        L[Batch Processing]
        M[Healthcare Metrics]
    end

    A --> C
    B --> C
    C --> D
    D --> F
    F --> G
    I --> J
    J --> F
    F --> L
    L --> M

    style A fill:#0277bd,color:#fff
    style C fill:#388e3c,color:#fff
    style F fill:#f57c00,color:#fff
    style I fill:#7b1fa2,color:#fff
    style L fill:#d32f2f,color:#fff



