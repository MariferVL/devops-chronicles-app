#!/bin/bash

sudo apt update -y
sudo apt install -y docker.io docker-compose
sleep 10
sudo docker run -d -p 5000:5000 \
    -e DB_USER=${db_user} \
    -e DB_PASS=${db_pass} \
    -e DB_NAME=${db_name} \
    -e DB_HOST=${db_host} \
    marifervl/devops-chronicles:latest