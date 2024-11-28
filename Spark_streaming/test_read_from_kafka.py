import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StringType

# Set environment variables
os.environ['PYSPARK_PYTHON'] = r'C:\Users\LENOVO\AppData\Local\Programs\Python\Python310\python.exe'
os.environ['PYSPARK_DRIVER_PYTHON'] = r'C:\Users\LENOVO\AppData\Local\Programs\Python\Python310\python.exe'

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaProducerTest") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.5.1") \
    .config("spark.driver.extraJavaOptions", "-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9090 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dlog4j.logger.org.apache.kafka=DEBUG") \
    .config("spark.sql.streaming.checkpointLocation", r'C:\check') \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.executor.extraJavaOptions", "-Dlog4j.logger.org.apache.kafka=DEBUG") \
    .getOrCreate()

# Define the schema of your Kafka messages (adjust as needed)
schema = StructType().add("value", StringType())

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("checkpointLocation", r"C:\check") \
    .option("startingOffsets", "latest") \
    .option("subscribe", "retour") \
    .load()

print("---------------MESSAGES READ FROM KAFKA ------------")

# Convert the value column from Kafka into a string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Process the data (example: simple select)
result_df = df.select("value")

# Write the result to console (for demonstration)
query = result_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

print("---------------STREAMING QUERY STARTED ------------")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("Streaming terminated by user")
finally:
    spark.stop()
