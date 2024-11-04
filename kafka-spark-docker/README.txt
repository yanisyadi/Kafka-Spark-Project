** Developers
    -> Zemir, Fatma Zohra
    -> Yadi, Yanis Atmane
    -> Gedeon, Ronald

** To run the data Pipeline
    - empty dir kafka-spark-docker/captors_data                        [if we re-run pipeline, this dir must not contain any file at the beginning]
    - docker-compose -f docker-compose.pipeline.yml up --build         [to build data pipeline until all containers are up & running]
    - docker-compose -f docker-compose.airflow.yml up airflow-init     [to init airflow env until `airflow-init-1 exited with code 0`]
    - docker-compose -f docker-compose.airflow.yml up --build          [to build airflow]
    ----------------------
    - docker exec -it consumer bash
        - less consumer.log                                            [to see loaded spark_data]
        - Shift + F                                                    [to follow the log entries]
    - docker exec -it producer bash
        - less filehandler.log
        - Shift + F
    - http://localhost:8081                                            [user/password: airflow/airflow, to navigate to airflow ui]
        -> activate captors_dag                                        [pause/unpause DAG captors_data]
            -> Graph View
        -> play Trigger Dag                                            [play button on the right screen of airflow-web-ui]
            -> trigger
      ---------------------

    - less consumer.log                                                [back to consumer.log to see spark data in logs]
    -------------------

** Treatment with Spark Queries
    - run
        - docker exec -it spark bash
        - spark-shell                                                  [--master spark://spark:7077]
    - scala> val df = spark.read.json("/opt/spark/*.json")
        - df.printSchema
        - df.show()
        - df.select("time", "customer", "device", "action").filter($"action" === "power on").show()
        - df.select("time", "customer", "device", "action").filter($"action" === "power off").show()
        - :q                                                    [to exit spark-shell]

** clean up
    - docker-compose -f docker-compose.airflow.yml down -v --rmi all
    - docker-compose -f docker-compose.pipeline.yml down -v --rmi all
------------------------





