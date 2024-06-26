#!/bin/bash
set -e
echo "Connected to remote server"
cd movies
echo "Pulled latest code"
git pull
echo "Removing all Docker containers"
docker rm -f $(docker ps -aq) || true
echo "Building Docker image"
docker build -t app .
echo "Running Docker container"
docker run -d --init -p 8000:8000 app
echo "Deployment completed"
