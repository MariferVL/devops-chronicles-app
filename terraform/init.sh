#!/bin/bash

sudo apt update -y
sudo apt install -y docker.io docker-compose
sleep 10
sudo docker run -d -p 5000:5000 \
    -e DB_USER=${var.db_user} \
    -e DB_PASS=${var.db_pass} \
    -e DB_NAME=${var.db_name} \
    -e DB_HOST=${aws_db_instance.devops_rds.address} \
    marifervl/devops-chronicles:latest