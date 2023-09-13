SHELL:=/bin/bash

install_conda:
	source ./scripts/install_conda.sh

install_docker:
	source ./scripts/install_docker.sh 

pg:
	pgcli -h localhost -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB}

buildup:
	docker-compose up -d
	@echo -n "Starting up the containers..."
	@sleep 30

connections: 
	source ./connectors/setup-connections.sh
	@echo -n "Getting the system ready..."
	@sleep 10

up: buildup connections

tup:
	docker-compose -f docker-compose-test.yml up -d 
	@echo -n "Starting up the containers..."
	@sleep 30

tdown:
	docker-compose -f docker-compose-test.yml down -v

down:
	docker-compose down -v

ci:
	docker exec test_suite pytest -p no:warnings -v

pg-src:
	curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '@./connectors/pg-src-connector.json'

s3-sink:
	curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '@./connectors/s3-sink.json'

tc:
	. ./tests/tc.sh
	@echo -n "Getting the system ready..."
	@sleep 10

tsetup: tup tc ci