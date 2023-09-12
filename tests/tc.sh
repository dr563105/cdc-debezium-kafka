#!/bin/bash

echo -e "\n"

#setup PG-source
echo -e "Setting up testing Postgres source...\n"

curl --include --request POST --header "Accept:application/json" \
    --header "Content-Type:application/json" \
    --url localhost:18083/connectors/ \
    --data '{    
        "name": "test-pg-src-connector",
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "1",
            "database.hostname": "'"${TEST_POSTGRES_USER}"'",
            "database.port": "5432",
            "database.user": "'"${TEST_POSTGRES_USER}"'",
            "database.password": "'"${TEST_POSTGRES_PASSWORD}"'",
            "database.dbname": "'"${TEST_POSTGRES_DB}"'",
            "database.server.name": "postgres",
            "database.include.list": "postgres",
            "topic.prefix": "test_debezium",
            "schema.include.list": "commerce",
            "decimal.handling.mode": "precise"
        }
    }'
echo -e "\n"

#Setup S3-sink
echo -e "Setting up S3-sink...\n"

curl --include --request POST --header "Accept:application/json" \
    --header "Content-Type:application/json" \
    --url localhost:18083/connectors/ \
    --data '{
        "name": "test-s3-sink",
        "config": {
            "connector.class": "io.aiven.kafka.connect.s3.AivenKafkaConnectS3SinkConnector",
            "aws.access.key.id": "'"${TEST_AWS_KEY_ID}"'",
            "aws.secret.access.key": "'"${TEST_AWS_SECRET_KEY}"'",
            "aws.s3.bucket.name": "'"${TEST_AWS_BUCKET_NAME}"'",
            "aws.s3.endpoint": "http://minio:9000",
            "aws.s3.region": "us-east-1",
            "format.output.type": "jsonl",
            "topics": "test_debezium.commerce.users, test_debezium.commerce.products",
            "file.compression.type": "none",
            "flush.size": "20",
            "file.name.template": "/{{topic}}/{{timestamp:unit=yyyy}}-{{timestamp:unit=MM}}-{{timestamp:unit=dd}}/{{timestamp:unit=HH}}/{{partition:padding=true}}-{{start_offset:padding=true}}.json"
        }
    }'
echo -e "\n"