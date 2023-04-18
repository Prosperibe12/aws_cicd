#!/usr/bin/env bash

virtualenv /home/ubuntu/aws_cicd/venv
source /home/ubuntu/aws_cicd/venv/bin/activate
pip install -r /home/ubuntu/aws_cicd/requirements.txt