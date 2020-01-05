from bfincher/alpine-python3:3.11

env PYTHONBUFFERED 1
arg BRANCH


workdir /hb
run wget https://github.com/bfincher/html_browser/tarball/${BRANCH} -O /tmp/hb.tgz && \
    tar -zxf /tmp/hb.tgz -C /hb --strip-components=1 && \
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
        -exec rm -rf '{}' + \
    && apk add --virtual .rundeps $runDeps && \
    cp /hb/html_browser/local_settings/local_settings_docker_sqlite.py /hb/html_browser/local_settings/local_settings.py && \
    cp /hb/html_browser/local_settings/local_settings_docker_sqlite.json /hb/html_browser/local_settings/local_settings.json && \
    apk del .git

copy root/ /

ENV APP_CONFIG="/config"

EXPOSE 80
VOLUME /config /data1 /data2
