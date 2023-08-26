FROM debezium/connect:latest

USER kafka

RUN curl --create-dirs -LO --output-dir /tmp/connector https://github.com/Aiven-Open/s3-connector-for-apache-kafka/releases/download/v2.13.0/s3-connector-for-apache-kafka-2.13.0.zip && \
    unzip -o /tmp/connector/s3-connector-for-apache-kafka-2.13.0.zip -d /tmp/connector && \
    mv /tmp/connector/s3-connector-for-apache-kafka-2.13.0 /kafka/connect/aiven-kafka-connect-s3 && \
    rm /tmp/connector/s3-connector-for-apache-kafka-2.13.0.zip