from bfincher/alpine-python3:3.12

env PYTHONBUFFERED 1
arg BRANCH


workdir /hb
run wget https://github.com/bfincher/html_browser/tarball/${BRANCH} -O /tmp/hb.tgz || \
    wget https://github.com/bfincher/html_browser/tarball/master -O /tmp/hb.tgz && \
    tar -zxf /tmp/hb.tgz -C /hb --strip-components=1 && \
    rm /tmp/hb.tgz && \
    rm -rf /hb/apache && \
    apk add --no-cache py3-pillow nginx && \
    apk add --no-cache --virtual .git git && \
    grep -v Pillow requirements.txt | pip install --no-cache -r /dev/stdin && \
    pip install --no-cache gunicorn==20.0.4 && \
    rm /etc/nginx/conf.d/default.conf && \
    mkdir -p /run/nginx && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + && \
    cp /hb/html_browser/docker_sqlite.env /hb/html_browser/.env && \
    apk del .git && \
    rm -rf /var/cache/apk/*

copy root/ /

ENV APP_CONFIG="/config"

EXPOSE 80
VOLUME /config /data1 /data2
