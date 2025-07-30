# 💊 Real-Time Pharmaceutical Data Streaming Pipeline
Extracted pharmaceutical registration data from Vietnam’s official drug portal (https://dichvucong.dav.gov.vn/congbothuoc/index)
This project implements a real-time data ingestion, transformation pipeline using the following tools and frameworks:

- **Apache Airflow** for DAG scheduling
- **Apache Kafka** for real-time message streaming
- **Apache Spark** for stream processing
- **PostgreSQL** for structured data storage
- **Docker Compose** for service orchestration

---

## 📁 Project Structure
```
DataStreamingFromDVCVer2/
│
├── dags/ # Airflow DAG definitions
│ ├── dvc_flow.py # Main DAG for handling DVC-triggered data
│ └── upsert_dag.py # DAG for upserting data to main DB
│
├── manager_crawl_time/ # Manage crawl timestamps
│ └── manager_time.py # Handles reading & writing crawl time from DB
│
├── pipelines/ # DVC data pipeline scripts
│ └── dvc_pipeline.py
│
├── postgres_data/ # (Optional) Postgres init SQL or volumes
│
├── realtime_processor/
│ ├── db/ # DB connection, creation, upsert logic
│ ├── kafka/ # Kafka consumer logic
│ ├── schema/ # PySpark schema definition
│ └── spark/ # Spark stream connection and transform logic
│ ├── connection.py # SparkSession connection
│ └── transform.py # Transform logic (JSON parse, explode, etc.)
│
├── script/ # Utility or helper scripts
│
├── docker-compose.yml # Full Docker environment (Kafka, Airflow, Postgres, etc.)
├── init.sql # SQL for DB setup
├── requirements.txt # Python dependencies
└── .gitignore

```

## 🚀 How It Works

1. **Airflow DAG (`dvc_flow.py`)** is triggered periodically:
   - Pulls the latest data using DVC
   - Compares `lastModificationTime` of records against the latest crawl time
   - Sends only new/updated records to Kafka topic `all_data`

2. **Kafka Producer** (in DAG) streams filtered data in JSON format.

3. **Spark Structured Streaming** (inside `spark/main.py`) reads from Kafka:
   - Parses the JSON using the schema
   - Transforms it into a clean DataFrame

4. **Spark → PostgreSQL**
   - Spark writes transformed batch data to PostgreSQL via JDBC
   - Data is inserted or upserted using custom logic in `upsert_to_main_table.py`

5. **Airflow DAG (`upsert_dag.py`)** updates the main table in DB with new records.

---

## 🧪 How to Run

> Make sure you have **Docker Desktop** installed.

### 1. Start All Services

```
docker-compose up --build
```

### 2. Access Services
Airflow UI: http://localhost:8080

PostgreSQL:

Host: localhost

Port: 5432

User: postgres

Password: 123456

### 3. Setup Spark and PostgreSQL Integration
🐘 Install PostgreSQL driver inside Spark container
```
docker exec -it spark-master pip install psycopg2-binary
```
#### 🗄️ Initialize Database Schema
```
docker exec -it spark-master python /opt/bitnami/spark/realtime_processor/db/init_db.py
```
#### ⚡ Start Spark Streaming Job
```
docker exec -it spark-master spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/realtime_processor/main.py
```
### 4. Trigger DAGs via Airflow
Open Airflow UI at http://localhost:8080

Trigger:

dvc_flow DAG to start crawling and pushing data to Kafka

upsert_dag to load data from temporary table to main table


## ✅ Features
Incremental data crawling based on lastModificationTime

Timezone-safe datetime comparison (all times converted to UTC)

Real-time streaming via Kafka + Spark

PostgreSQL upsert logic for deduplication

Modular codebase for easy maintenance

## 📌 Future Improvements
Add monitoring for DAG/task failures

Implement alerting for pipeline downtime

Build a frontend dashboard using React + Chart.js or D3.js

Optimize Spark performance for large datasets

## 🛠️ Tech Stack
Component	Tool
Orchestration	Apache Airflow
Data Versioning	DVC
Message Queue	Apache Kafka
Stream Processing	Apache Spark
Database	PostgreSQL
Deployment	Docker Compose
Language	Python (3.8+)

## 👨‍💻 Author
Diu Nguyen
Data Engineer / Fullstack Developer
🇻🇳 Passionate about data pipelines, streaming systems, and beautiful dashboards.

## 📄 License
This project is for educational and personal learning purposes.

