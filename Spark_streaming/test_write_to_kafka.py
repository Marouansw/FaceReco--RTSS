import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Set environment variables
os.environ['PYSPARK_PYTHON'] = r'C:\Users\LENOVO\AppData\Local\Programs\Python\Python310\python.exe'
os.environ['PYSPARK_DRIVER_PYTHON'] = r'C:\Users\LENOVO\AppData\Local\Programs\Python\Python310\python.exe'

try:
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("KafkaProducerTest") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.5.1") \
        .config("spark.driver.extraJavaOptions", "-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9090 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dlog4j.logger.org.apache.kafka=DEBUG") \
        .config("spark.executor.extraJavaOptions", "-Dlog4j.logger.org.apache.kafka=DEBUG") \
        .getOrCreate()

    # Create a simple DataFrame
    data = [("key1", "PULL UP")]
    columns = ["key", "value"]
    df = spark.createDataFrame(data, columns)

    # Write DataFrame to Kafka
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "retour") \
        .mode("append") \
        .save()

    print("Messages sent to Kafka topic")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    # Stop Spark session
    if 'spark' in locals():
        spark.stop()