#!/bin/bash

sudo rm /etc/nginx/nginx.conf;
sudo cp nginx.conf /etc/nginx/nginx.conf;
sudo service nginx stop;
sudo service nginx start;

gunicorn --paste ngse.ini -b 0.0.0.0:8080 --workers=3 &;