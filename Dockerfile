FROM selenium/standalone-chrome

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    python \
    python3-pip
RUN python3 -m pip install -U selenium
COPY . .
CMD python3 amazon_add_to_cart.py