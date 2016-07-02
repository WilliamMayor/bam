FROM selenium/standalone-chrome-debug

RUN \
    apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip && \
    apt-get clean autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN  mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH $PYTHONPATH:/usr/src/app

ADD . /usr/src/app
RUN pip3 install -r requirements.txt

CMD ["/usr/src/app/fetch.sh"]
