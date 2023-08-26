SHELL:=/bin/bash

install_conda:
	source ./scripts/install_conda.sh

install_docker:
	source ./scripts/install_docker.sh 

pg:
	pgcli -h localhost -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB}

up:
	docker-compose up -d

# remove-minio:
# 	sudo rm -rf minio/

compose-down:
	docker-compose down -v

down:
	compose-down

s3-sink:
	curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '@./connectors/pg-src-connector.json'

pg-src:
	curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '@./connectors/s3-sink.json'

connectors: pg-src s3-sink