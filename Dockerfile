from bfincher/alpine-python3:3.11

env PYTHONBUFFERED 1
arg BRANCH


workdir /hb
run mkdir -p /hb/html_browser && \
    apk add --no-cache py3-pillow nginx git && \
    pip install --no-cache gunicorn==20.0.4 && \
    rm /etc/nginx/conf.d/default.conf && \
    mkdir -p /run/nginx && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + && \
    apk add --virtual .rundeps $runDeps && \
    cp /hb/html_browser/cygwin.env /.env

copy root/ /

ENV APP_CONFIG="/config"

EXPOSE 80
VOLUME /config /data1 /data2
