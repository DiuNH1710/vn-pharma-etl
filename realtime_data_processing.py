#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, explode
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, ArrayType
import psycopg2
import logging
import time


def create_table():
    conn = None
    try:
        # Kết nối đến PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Tạo bảng nếu chưa tồn tại
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmaceutical_data (
            idThuoc INTEGER, 
            phanLoaiThuocEnum INTEGER,
            tenCongTyDangKy TEXT,
            diaChiDangKy TEXT,
            nuocDangKy TEXT,
            congTyDangKyId INTEGER,
            tenCongTySanXuat TEXT,
            diaChiSanXuat TEXT,
            nuocSanXuat TEXT,
            congTySanXuatId INTEGER, 
            fullAddress TEXT,
            soDangKy TEXT ,
            soDangKyCu TEXT,
            tenThuoc TEXT,
            dotCap TEXT,
            ngayCapSoDangKy TIMESTAMP,
            ngayHetHanSoDangKy TIMESTAMP,
            ngayGiaHanSoDangKy TIMESTAMP,
            soQuyetDinh TEXT,
            thongTinRutSoDangKy TEXT,
            dangBaoChe TEXT,
            dongGoi TEXT,
            hamLuong TEXT,
            hoatChatChinh TEXT,
            tieuChuan TEXT,
            tieuChuanId TEXT,
            tuoiTho TEXT,
            creationTime TIMESTAMP,
            lastModificationTime TIMESTAMP,
            crawlTime TIMESTAMP
           
        );
        """)
        conn.commit()

        print("Table created successfully in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()


def transform_dvc_data(spark_df):
    print("Starting transformation of DVC data...")

    # Split lat_long struct into separate columns
    transformed_df = spark_df.withColumn("phanLoaiThuocEnum", col("phanLoaiThuocEnum").cast("int")) \
                                .withColumn("idThuoc", col("idThuoc").cast("int"))\
                                .withColumn("congTyDangKyId", col("congTyDangKyId").cast("int"))\
                                .withColumn("congTySanXuatId", col("congTySanXuatId").cast("int"))\

    return transformed_df

def create_spark_connection():
    s_conn = None

    try:
        s_conn = (SparkSession.builder
                  .appName('KafkaDVCComsumer')
                  .master("spark://spark-master:7077")
                  .config("spark.jars", "/opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar,"
                                        "/opt/bitnami/spark/jars/kafka-clients-3.5.0.jar,"
                                        "/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar,"
                                        "/opt/bitnami/spark/jars/commons-pool2-2.11.1.jar,"
                                        "/opt/bitnami/spark/jars/postgresql-42.2.18.jar")
                  .config("spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar")
                  .config("spark.executor.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar")
                  .getOrCreate())

        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")
    return s_conn

def connect_to_kafka(spark_conn):
    spark_df = None
    try:
        spark_df=spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'kafka:9092') \
            .option('subscribe', 'all_data')\
            .option('startingOffsets', 'latest')\
            .load()
        logging.info("kafka dataframe created successfully")
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because:{e}")

    return spark_df

def write_to_postgres(batch_df, batch_id, postgres_table_name):
    print(f"Processing batch {batch_id}")
    batch_df = batch_df.drop("id")
    batch_df = batch_df.dropDuplicates(["soDangKy"])

    batch_df.show(1)  # Show the first 5 rows of the batch for inspection
    # use localhost or postgres??

    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5432/postgres")\
        .option("dbtable", f"public.{postgres_table_name}") \
        .option("user", "postgres") \
        .option("password", "123456") \
        .mode("append") \
        .save()

def create_selection_df_from_kafka(spark_df):
    # Define the schema that matches your table structure
    schema = StructType([
        StructField("idThuoc", StringType(), True),
        StructField("phanLoaiThuocEnum", StringType(), True),
        StructField("tenCongTyDangKy", StringType(), True),
        StructField("diaChiDangKy", StringType(), True),
        StructField("nuocDangKy", StringType(), True),
        StructField("congTyDangKyId", StringType(), True),
        StructField("tenCongTySanXuat", StringType(), True),
        StructField("diaChiSanXuat", StringType(), True),
        StructField("nuocSanXuat", StringType(), True),
        StructField("congTySanXuatId", StringType(), True),
        StructField("fullAddress", StringType(), True),
        StructField("soDangKy", StringType(), True),  # PRIMARY KEY, so it cannot be null
        StructField("soDangKyCu", StringType(), True),
        StructField("tenThuoc", StringType(), True),
        StructField("dotCap", StringType(), True),
        StructField("ngayCapSoDangKy", TimestampType(), True),
        StructField("ngayHetHanSoDangKy", TimestampType(), True),
        StructField("ngayGiaHanSoDangKy", TimestampType(), True),
        StructField("soQuyetDinh", StringType(), True),
        StructField("thongTinRutSoDangKy", StringType(), True),
        StructField("dangBaoChe", StringType(), True),
        StructField("dongGoi", StringType(), True),
        StructField("hamLuong", StringType(), True),
        StructField("hoatChatChinh", StringType(), True),
        StructField("tieuChuan", StringType(), True),
        StructField("tieuChuanId", StringType(), True),
        StructField("tuoiTho", StringType(), True),
        StructField("creationTime", TimestampType(), True),
        StructField("lastModificationTime", TimestampType(), True),
        StructField("crawlTime", TimestampType(), True)
    ])

    # Extract the JSON data from the Kafka stream and apply the schema
    parsed_df = spark_df.selectExpr("CAST(value AS STRING) as json_str") \
        .withColumn("data", from_json(col("json_str"), ArrayType(schema))) \
        .withColumn("data", explode(col("data")))  # explode từng object trong array

    # B3: Chọn các cột cụ thể từ object đã explode
    selected_df = parsed_df.select(col("data.*"),)

    return selected_df

if __name__ == "__main__":
    print("Welcome to DataMaking !!!")
    print("Real-Time Data Processing Application Started ...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

    create_table()

    spark_conn = create_spark_connection()
    if spark_conn is not None:
        # connect to kafka with spark connection
        spark_df = connect_to_kafka(spark_conn)
        print("Printing Schema of spark_df: ")

        spark_df.printSchema()

        selection_df = create_selection_df_from_kafka(spark_df)

        transformed_df = transform_dvc_data(selection_df)

        transformed_df.writeStream \
            .foreachBatch(lambda batch_df, batch_id: write_to_postgres(batch_df, batch_id, "pharmaceutical_data")) \
            .start() \
            .awaitTermination()
