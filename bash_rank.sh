# /bin/bash

docker run --privileged -d -p 4444:4444 --shm-size 2g selenium/standalone-chrome 
sleep 20
python rank.py 
docker ps | grep -o '^[a-z0-9A-Z]\{12\}' | xargs docker kill $1