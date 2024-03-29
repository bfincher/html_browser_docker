THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

USERID=1000
GROUPID=1000
USERNAME=$(getent passwd $USERID | gawk -F':' '{ print $1}')
GROUPNAME=$(getent group $GROUPID | gawk -F':' '{ print $1}')

if [ -z $VIRTUAL_ENV ]; then
    image_name=bfincher/html_browser:alpine-sqlite
    container_name=html_browser_alpine_sqlite
    CONFIG=${THIS_DIR}/config
else
    image_name=bfincher/$(basename $VIRTUAL_ENV):alpine-sqlite
    container_name=$(basename $VIRTUAL_ENV)_alpine_sqlite
    CONFIG=${THIS_DIR}/${container_name}_config
fi

version=$(./getVersion.sh)

image_name=${image_name}_${version}

if [ ! -d $CONFIG ]; then
    mkdir $CONFIG
fi

chown -R ${USERNAME}:${GROUPNAME} $CONFIG


if [ $# -eq 1 ]; then
    port=$1
else
    port=8000
fi

docker run -d \
    -p $port:80 \
    -v ${CONFIG}:/config \
    -v /Volumes/data1:/data1 \
    -e USERID=$USERID \
    -e GROUPID=$GROUPID \
    -e USERNAME=$USERNAME \
    -e GROUPNAME=$GROUPNAME \
    -e HOMEDIR=/hb \
    --name=$container_name \
    --restart unless-stopped \
    $image_name
