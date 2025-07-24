import logging
from pyspark.sql import SparkSession


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
        return s_conn
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")
        return None