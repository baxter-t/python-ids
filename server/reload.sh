sudo docker stop $(sudo docker ps -aq)
sudo docker build -t test-server .
sudo docker run -d -p 80:80 test-server
