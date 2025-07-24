import logging
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import ArrayType, StructField, StringType, StructType, TimestampType
from realtime_processor.schema.drugs_schema import get_drugs_schema


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


def create_selection_df_from_kafka(spark_df):
    # Define the schema that matches your table structure
    schema = get_drugs_schema()

    # Extract the JSON data from the Kafka stream and apply the schema
    parsed_df = spark_df.selectExpr("CAST(value AS STRING) as json_str") \
        .withColumn("data", from_json(col("json_str"), ArrayType(schema))) \
        .withColumn("data", explode(col("data")))

    selected_df = parsed_df.select(col("data.*"),)

    return selected_df