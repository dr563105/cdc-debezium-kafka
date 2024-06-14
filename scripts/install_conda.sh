#!/bin/bash

cd ~
wget -q https://github.com/conda-forge/miniforge/releases/download/23.11.0-0/Miniforge3-23.11.0-0-Linux-x86_64.sh -O Miniforge3-23.11.0-0-Linux-x86_64.sh
bash Miniforge3-23.11.0-0-Linux-x86_64.sh -b
~/miniforge3/bin/conda init $SHELL_NAME
rm Miniforge3-23.11.0-0-Linux-x86_64.sh
cd ~/cdc-debezium-kafka