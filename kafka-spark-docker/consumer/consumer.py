import json
import logging
import os
import sys
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row

# list of kafka messages
messages = []

# Setting env variables for spark
os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3.11'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3.11'

# Create Spark Session & Context
spark = SparkSession.builder.appName("KafkaSpark").master("spark://spark:7077").getOrCreate()
sc = SparkContext.getOrCreate()
sc.setLogLevel('WARN')


def main():
    logging.basicConfig(filename='/app/consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Debugging env settings")
    logging.info(f"python path: {sys.executable}")
    logging.info("Python executable: %s", sys.executable)
    logging.info("PYSPARK_PYTHON: %s", os.getenv('PYSPARK_PYTHON'))
    logging.info("PYSPARK_DRIVER_PYTHON: %s", os.getenv('PYSPARK_DRIVER_PYTHON'))
    logging.info("SPARK_HOME: %s", os.getenv('SPARK_HOME'))
    logging.info("PATH: %s", os.getenv('PATH'))

    load_from_kafka2_spark("clogs")     # Start consuming kafka messages
    logging.info("Completed loading data from kafka to spark")

def get_spark_data(data):
    # RDD creation
    rdd = sc.parallelize(data.items()) # rdd here is a list of tuples
    return dict(rdd.collect())  # convert rdd back to a dict

def process_with_spark():
    logging.info("Processing spark data")
    if not messages:
        logging.error(" No messages were collected from kafka")
        return
    df = spark.createDataFrame([Row(**message) for message in messages])    # Convert messages into a DataFrame
    if df.rdd.isEmpty():
        logging.info("The DataFrame is empty")
    else:
        df.createOrReplaceTempView("device_actions")    # Register the DataFrame as a temporary SQL table/view
        query = spark.sql("SELECT customer FROM device_actions WHERE action = 'power on'")  # SQL query
        query.show(truncate=False)    # Show the query
    logging.info("Completed processing spark data")

def load_from_kafka2_spark(topic):
    """ function that read from kafka topic using brokers & then sends it to spark """

    # Kafka consumer creation
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True, #
        group_id='my_group', #
        # consumer_timeout_ms=150000  # set kafka messages consuming to 2.5 min
        # value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    if topic not in consumer.subscription():
        consumer.subscribe([topic])
    logging.info("Kafka consumer initialized and subscribed to topic")
    logging.info("starting consuming kafka messages")

    try:
        i = 0
        logging.info(f"Loading data into Spark ...")  # to log kafka message to consumer.log
        for msg in consumer:
            data = msg.value.decode('utf-8')
            i+=1

            kafka_data = json.loads(data)   # Get kafka_data
            messages.append(kafka_data)
            logging.info(f"{i}:\t{get_spark_data(kafka_data)}")
            time.sleep(1)   # Sleep 1 sec to avoid busy waiting
        logging.info("Completed loading data into Spark\n")

    except KafkaError as err:
        logging.error(f"Kafka error: {err}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        sys.exit(0)
    finally:
        consumer.close()
        logging.info("exiting consumer & processing Spark data...")
        # process_with_spark()    # process spark data after exiting loop


if __name__ == "__main__":
    main()
