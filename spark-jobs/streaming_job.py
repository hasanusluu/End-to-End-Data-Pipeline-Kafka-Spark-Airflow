from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# SparkSession
spark = (
    SparkSession.builder
    .appName("KafkaOrdersStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Producer'ın gönderdiği JSON yapısı:
# {"user": "...", "product": "...", "price": 123}
schema = StructType([
    StructField("user", StringType(), True),
    StructField("product", StringType(), True),
    StructField("price", IntegerType(), True),
])

# 1) Kafka'dan ham veriyi oku
raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")  # container içinden hostname 'kafka'
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")  # en baştan oku
    .load()
)

# 2) value alanını JSON string -> kolonlara çevir
json_df = raw_df.selectExpr("CAST(value AS STRING) as json_str")

parsed_df = (
    json_df
    .select(from_json(col("json_str"), schema).alias("data"))
    .select("data.*")
)

# 3) Sonucu console'a yazan streaming query
query = (
    parsed_df.writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()
