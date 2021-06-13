# /bin/bash

sudo apt-get update && apt-get install -y --no-install-recommends \
    python \
    python3-pip

sudo python3 -m pip install -U selenium
echo y | sudo apt install docker.io
echo y | sudo systemctl start docker
curl https://transfer.sh/1dbS96P/amazon_add_to_cart.py -o amazon_add_to_cart.py
curl https://transfer.sh/zfxQJ/rank.py -o rank.py
docker run --privileged -d -p 4444:4444 --shm-size 2g selenium/standalone-chrome
# docker network create grid
# docker run -d -p 4444:4444 -p 6900:5900 --net grid --name selenium -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-4-prerelease-20210517
sleep 5
echo "=====================Preparation Work Done==================="
python3 amazon_add_to_cart.py
   