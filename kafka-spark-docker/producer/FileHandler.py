import time
import logging

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer  # package for monitoring a directory

from producer.Producer import Producer


def main():
    logging.basicConfig(filename='/app/filehandler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %('
                                                                               'message)s')
    directory = "/app/captors_data/"  # docker directory to watch which is relative to working dir src/producer
    observer = Observer()  # watchdog observer instance to monitor the directory
    file_handler = FileHandler(Producer())  # Dependency Injection
    observer.schedule(file_handler, path=directory, recursive=False)  # schedule the FileHandler to monitor dir files
    observer.start()  # start the observer in separate thread to begin monitoring directory for file creation events.

    try:
        logging.info(f"\nMonitoring directory {directory} for new files ...")
        while True:
            time.sleep(1)   # Sleep to keep the script running and avoid busy waiting
    except KeyboardInterrupt:
        logging.info("Stopping observer monitoring ...")
    finally:
        observer.stop()
        observer.join()  # to have the main thread wait until the observer's event loop terminates
        file_handler.producer.close()   # closing the kafka producer


class FileHandler(FileSystemEventHandler):
    """ class that is an event handler for monitoring file system events """

    def __init__(self, producer: Producer):
        self.producer = producer  # Injecting Producer dependency in the constructor

    def on_created(self, event):
        if event.is_directory:
            return
        time.sleep(5)  # timeout to allow the file to be completely written in dir
        file_path = event.src_path
        logging.info(f"\nNew file detected: {file_path}")

        self.producer.write_to_kafka("clogs", file_path)  # create & then write to the topic


if __name__ == "__main__":
    main()
