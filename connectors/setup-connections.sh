#!/bin/bash

echo -e "\n"

#setup PG-source
echo -e "Setting up Postgres source...\n"

curl --include --request POST --header "Accept:application/json" \
    --header "Content-Type:application/json" \
    --url localhost:8083/connectors/ \
    --data '{    
        "name": "pg-src-connector",
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "1",
            "database.hostname": "'"${POSTGRES_USER}"'",
            "database.port": "5432",
            "database.user": "'"${POSTGRES_USER}"'",
            "database.password": "'"${POSTGRES_PASSWORD}"'",
            "database.dbname": "'"${POSTGRES_DB}"'",
            "database.server.name": "postgres",
            "database.include.list": "postgres",
            "topic.prefix": "debezium",
            "schema.include.list": "commerce",
            "decimal.handling.mode": "precise"
        }
    }'
echo -e "\n"

#Setup S3-sink
echo -e "Setting up S3-sink...\n"

curl --include --request POST --header "Accept:application/json" \
    --header "Content-Type:application/json" \
    --url localhost:8083/connectors/ \
    --data '{
        "name": "s3-sink",
        "config": {
            "connector.class": "io.aiven.kafka.connect.s3.AivenKafkaConnectS3SinkConnector",
            "aws.access.key.id": "'"${AWS_KEY_ID}"'",
            "aws.secret.access.key": "'"${AWS_SECRET_KEY}"'",
            "aws.s3.bucket.name": "'"${AWS_BUCKET_NAME}"'",
            "aws.s3.endpoint": "http://minio:9000",
            "aws.s3.region": "us-east-1",
            "format.output.type": "jsonl",
            "topics": "debezium.commerce.users,debezium.commerce.products",
            "file.compression.type": "none",
            "flush.size": "20",
            "file.name.template": "/{{topic}}/{{timestamp:unit=yyyy}}-{{timestamp:unit=MM}}-{{timestamp:unit=dd}}/{{timestamp:unit=HH}}/{{partition:padding=true}}-{{start_offset:padding=true}}.json"
        }
    }'
echo -e "\n"