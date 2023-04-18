#!/usr/bin/bash
sudo cp /home/ubuntu/aws_cicd/gunicorn/gunicorn.socket  /etc/systemd/system/gunicorn.socket
sudo cp /home/ubuntu/aws_cicd/gunicorn/gunicorn.service  /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
