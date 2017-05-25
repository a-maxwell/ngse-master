#!/bin/bash

echo "Updating some files..."

sudo apt-get update

echo "Installing some dependencies..."

sudo apt-get install -y python-pip postgresql libpq-dev nginx supervisor

echo "Installing Virtual Environment for Python 2.7..."

pip install virtualenv

echo "Done! Proceed to sequence #2 on the installation guide."