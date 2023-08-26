#!/bin/bash

mkdir -p input_data && cd input_data
wget -q https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz && gzip -d green_tripdata_2019-01.csv.gz
wget -q https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
cd ~/de_zc2023