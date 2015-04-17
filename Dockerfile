FROM ubuntu

RUN \
    apt-get update && \
    apt-get install -y \
        python2.7 \
        python2.7-dev \
        python-pip \
        firefox \
        ca-certificates \
        xfonts-100dpi \
        xfonts-75dpi \
        xfonts-scalable \
        xfonts-cyrillic \
        xvfb --no-install-recommends && \
    apt-get clean autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV DISPLAY :99

ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

CMD ["bash"]
