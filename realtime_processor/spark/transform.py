from pyspark.sql.functions import col


def transform_dvc_data(spark_df):
    print("Starting transformation of DVC data...")

    # Split lat_long struct into separate columns
    transformed_df = spark_df.withColumn("phanLoaiThuocEnum", col("phanLoaiThuocEnum").cast("int")) \
                                .withColumn("idThuoc", col("idThuoc").cast("int"))\
                                .withColumn("congTyDangKyId", col("congTyDangKyId").cast("int"))\
                                .withColumn("congTySanXuatId", col("congTySanXuatId").cast("int"))\

    return transformed_df