from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, StructType, StructField
import base64
import requests
import json
import gzip
from io import BytesIO
from PIL import Image
import numpy as np

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaImageProcessing") \
    .getOrCreate()

# Define schema for the incoming Kafka message
schema = StructType([
    StructField("key", StringType(), True),
    StructField("value", StringType(), True)
])

# Function to send image to the Flask API and get the result
def process_image(encoded_image):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(encoded_image)
        image = BytesIO(image_data)
        with gzip.GzipFile(fileobj=image, mode='rb') as img:
            # Send the image to the API
            url = 'http://127.0.0.1:5000/get_infos'
            files = {"image": img}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            return json.dumps(response.json())  # Return the result as a JSON string
        else:
            return json.dumps({"error": "API call failed", "status_code": response.status_code})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Register the function as a UDF
process_image_udf = udf(process_image, StringType())

# Read from the Kafka topic "aller"
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "aller") \
    .load()

# Extract the value (encoded image) and process it
image_df = df.selectExpr("CAST(value AS STRING)")

# Process the image using the UDF
result_df = image_df.withColumn("result", process_image_udf(col("value")))

# Write the results to the Kafka topic "retour"
query = result_df.selectExpr("CAST(result AS STRING) AS value").writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "retour") \
    .option("checkpointLocation", r"C:\Users\LENOVO\Desktop\ETUDES\Master DS\S2\Deep Learning\Face-Recognition--DL\Spark_streaming\tmp") \
    .start()

query.awaitTermination()
