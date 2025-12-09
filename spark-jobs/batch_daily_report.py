from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sum, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# SparkSession
spark = (
    SparkSession.builder
    .appName("DailyReportBatch")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Schema
schema = StructType([
    StructField("user", StringType(), True),
    StructField("product", StringType(), True),
    StructField("price", IntegerType(), True),
])

# Read from Kafka in Batch mode (reads all available data)
# Note: In a real scenario, you would manage offsets to read only new data.
df = (
    spark.read
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")
    .option("endingOffsets", "latest")
    .load()
)

# Parse JSON
json_df = df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = (
    json_df
    .select(from_json(col("json_str"), schema).alias("data"))
    .select("data.*")
)

# Calculate Report: Total Sales per Product
report_df = (
    parsed_df
    .groupBy("product")
    .agg(
        count("*").alias("total_orders"),
        sum("price").alias("total_revenue")
    )
)

print("----------- DAILY REPORT -----------")
report_df.show()
print("------------------------------------")

spark.stop()
