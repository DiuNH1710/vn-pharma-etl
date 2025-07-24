def write_to_postgres(batch_df, batch_id, postgres_table_name):
    print(f"Processing batch {batch_id}")
    batch_df = batch_df.drop("id")
    batch_df = batch_df.dropDuplicates(["soDangKy"])

    batch_df.show(1)  # Show the first 1 rows of the batch for inspection
    # use localhost or postgres??

    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5432/postgres")\
        .option("dbtable", f"public.{postgres_table_name}") \
        .option("user", "postgres") \
        .option("password", "123456") \
        .mode("append") \
        .save()

