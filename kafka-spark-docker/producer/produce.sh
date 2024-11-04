#!/bin/bash

# Wait for 10 sec before running consumer.py
for ((i=9; i>=0; i--))
do
  echo -ne "\r\e[32m running producer in $i seconds\e[0m"
  sleep 1
done
echo -e "\n"

# run producer.py
exec python /app/producer/FileHandler.py