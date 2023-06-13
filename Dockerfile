from bfincher/alpine-python3:3.18

env PYTHONBUFFERED 1
arg BRANCH


workdir /hb
run echo "branch = ${BRANCH}" && \
    wget https://github.com/bfincher/html_browser/tarball/${BRANCH} -O /tmp/hb.tgz || \
    wget https://github.com/bfincher/html_browser/tarball/master -O /tmp/hb.tgz && \
    tar -zxf /tmp/hb.tgz -C /hb --strip-components=1 && \
    rm /tmp/hb.tgz && \
    apk add --no-cache py3-pillow && \
    apk add --no-cache --virtual .builddeps git gcc libc-dev linux-headers python3-dev && \
    pip install --no-cache uwsgi==2.0.21 && \
    grep -v Pillow requirements.txt | pip install --no-cache -r /dev/stdin && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + && \
    cp /hb/docker_sqlite.env /hb/.env && \
    apk del .builddeps && \
    rm -rf /var/cache/apk/*

copy root/ /

ENV APP_CONFIG="/config"

EXPOSE 80
VOLUME /config /data1 /data2
