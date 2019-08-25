if [ -z $VIRTUAL_ENV ]; then
    image_name=bfincher/html_browser:alpine-sqlite_d
else
    image_name=bfincher/$(basename $VIRTUAL_ENV):alpine-sqlite_d
fi
docker build -t $image_name .
