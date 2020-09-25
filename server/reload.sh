docker stop $(docker ps -aq)
docker build -t test-server .
docker run -d -p 80:80 test-server
