#!/bin/bash

# Function to print an ERROR message
handle_error() {
  echo "Error: $1"
  exit 1
}

# Wait for 15 sec before running consumer.py
for ((i=14; i>=0; i--))
do
  echo -ne "\r\e[32m running consumer in $i seconds\e[0m"
  sleep 1
done
echo -e "\n"

# run python consumer.py
if ! python /app/consumer/consumer.py; then
  handle_error "Failed to execute consumer.py"
fi

#echo "consumer.py script completed successfully."