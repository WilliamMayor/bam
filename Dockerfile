FROM ubuntu

RUN \
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main' 9.4 > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install --assume-yes --force-yes \
        postgresql-9.4 \
        postgresql-server-dev-9.4 && \
    apt-get install -y \
        g++ \
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

RUN  mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONPATH $PYTHONPATH:/usr/src/app

ADD . /usr/src/app
RUN pip install -r requirements.txt

CMD ["bash"]
