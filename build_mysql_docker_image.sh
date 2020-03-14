version=$(cat version.txt)
image_name=bfincher/html_browser:alpine-mysql_$version
docker build --build-arg version=$version -t $image_name -f Dockerfile_mysql . 
