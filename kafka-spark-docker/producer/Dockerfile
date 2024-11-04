FROM python:3.11-slim

# Install bash & less for script exec, logs file reading, && clean up the cached package lists
RUN apt-get update && apt-get install -y bash less && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY producer/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p  /app/captors /app/captors_data

COPY captors/ /app/captors/

COPY producer/ /app/producer

RUN chmod +x /app/producer/produce.sh

# set python path to docker working directory
ENV PYTHONPATH=/app

CMD ["/app/producer/produce.sh"]