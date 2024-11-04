FROM python:3.11-slim

#Install wget & tar
RUN apt-get update && apt-get install -y curl wget tar && apt-get clean

RUN wget https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u362-b09/OpenJDK8U-jdk_x64_linux_hotspot_8u362b09.tar.gz && \
    tar -xzf OpenJDK8U-jdk_x64_linux_hotspot_8u362b09.tar.gz -C /opt && \
    rm OpenJDK8U-jdk_x64_linux_hotspot_8u362b09.tar.gz

# Check java installation
RUN printf "\e[31m content of /opt directory:\e[0m\n" && ls /opt && ls /opt/jdk8u362-b09/bin

# Set JAVA_HOME env as pyspark depends on java runtime
ENV JAVA_HOME=/opt/jdk8u362-b09
ENV PATH=$JAVA_HOME/bin:$PATH

# Update alternatives to use the newly installed Java
RUN update-alternatives --install /usr/bin/java java /opt/jdk8u362-b09/bin/java 1 && \
    update-alternatives --install /usr/bin/javac javac /opt/jdk8u362-b09/bin/javac 1

# Install bash & less for script exec & logs file reading, && clean up the cached package lists
RUN apt-get update && apt-get install -y bash less && rm -rf /var/lib/apt/lists/*

# Install ps command
RUN apt-get update && apt-get install -y procps

# Set PYSPARK_PYTHON to match installation -which python
ENV PYSPARK_PYTHON=/usr/local/bin/python3.11

WORKDIR /app

COPY consumer/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/consumer

RUN mkdir /app/df

COPY consumer/ /app/consumer

RUN chmod +x /app/consumer/consume.sh

ENV PYTHONPATH=/app

CMD ["/app/consumer/consume.sh"]