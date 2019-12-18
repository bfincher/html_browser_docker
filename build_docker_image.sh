if [ -z $VIRTUAL_ENV ]; then
    image_name=bfincher/html_browser:alpine-sqlite
else
    image_name=bfincher/$(basename $VIRTUAL_ENV):alpine-sqlite
fi

branch_name=$(git symbolic-ref -q HEAD)
branch_name=${branch_name##refs/heads/}
branch_name=${branch_name:-HEAD}

docker build --build-arg BRANCH=$branch_name -t $image_name .
