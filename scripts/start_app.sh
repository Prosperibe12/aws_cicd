#!/usr/bin/bash 

sed -i 's/\[]/\["54.145.160.241"]/' /home/ubuntu/aws_cicd/project_core/settings.py

python3 manage.py makemigrations     
python3 manage.py migrate 
sudo service gunicorn restart
sudo service nginx restart
#sudo tail -f /var/log/nginx/error.log
#sudo systemctl reload nginx
#sudo tail -f /var/log/nginx/error.log
#sudo nginx -t
#sudo systemctl restart gunicorn
#sudo systemctl status gunicorn
#sudo systemctl status nginx
# Check the status
#systemctl status gunicorn
# Restart:
#systemctl restart gunicorn
#sudo systemctl status nginx
