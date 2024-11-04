import json
import threading
import logging

from kafka import KafkaProducer


class Producer:
    """ Singleton class: to create only one instance of that class for watchdog """
    _instance = None
    _lock = threading.Lock()    # lock to ensure thread-safe singleton creation

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Producer, cls).__new__(cls)
                    cls._instance._initialize_producer()
        return cls._instance

    def _initialize_producer(self, bootstrap_servers='kafka:9092'):     # kafka Broker
        self.bootstrap_servers = bootstrap_servers
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
                                            # value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def close(self):
        self.kafka_producer.close()

    def error_callback(self, exc):
        raise Exception(f"Error while sending data to kafka: {str(exc)}")

    def write_to_kafka(self, topic: str, filepath: str):
        """ function that writes messages to kafka using broker """
        logging.basicConfig(filename='producer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %('
                                                                                'message)s')

        with open(filepath) as f:
            for line in f:  # read the file line by line & remove trailing white space & '\n' character
                message = line.strip()
                if message:
                    try:
                        self.kafka_producer.send(topic, message.encode('utf-8'))  # .add_callback(self.error_callback)
                        logging.info(f"Successfully sent message: {message} to kafka topic: {topic}")
                    except Exception as e:
                        logging.error(f"Fail to produce message to kafka topic: {topic} due to error: {str(e)}")
            self.kafka_producer.flush()
            # self.kafka_producer.close()   # producer needs to keep running for watchdog
