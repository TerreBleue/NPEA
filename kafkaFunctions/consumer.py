from kafka import KafkaConsumer
import sys
import os
from pyspark.sql import SparkSession
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mongodbFunctions import insert_noise_data

consumer_day = KafkaConsumer(
    'center', 'north', 'east', 'south', 'west',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='my_group'
)

print("Waiting for messages...")
spark = SparkSession.builder.appName("KafkaToSpark").getOrCreate()

for message in consumer_day:
    doc = json.loads(message.value.decode('utf-8'))
    df = spark.createDataFrame([doc])
    print("####################")
    df.show()
    print("####################")
    insert_noise_data(doc)