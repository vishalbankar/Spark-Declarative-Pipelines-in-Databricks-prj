from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp
from pyspark.sql.functions import md5,concat_ws, sha2


# source path configuration here you can add your S3 bucket folder path
SOURCE_PATH = "/Volumes/transportation/bronze/raw_s3_data/city"

@dp.materialized_view(
    name="transportation.bronze.city",
    comment="City Raw Data Processing",
    table_properties={
        "quality": "bronze",
        "layer": "bronze",
        "source_format": "csv",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    }
)
def city_bronze():
    # function load data from volume/s3 bucket/ to dataframe
    # mode set to permissive to ignore bad records
    df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").option("mode", "PERMISSIVE").option("mergeSchema", "true").option("columnNameOfCorruptRecord","_corrupt_record").load(SOURCE_PATH)

# here i added metadata column which useful for later audit purpose
    df = df.withColumn("file_name", col("_metadata.file_path")).withColumn("ingest_datetime", current_timestamp())
    
    return df 
