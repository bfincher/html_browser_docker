#!/bin/bash

branch_name=$(git symbolic-ref -q HEAD)
branch_name=${branch_name##refs/heads/}
branch_name=${branch_name:-HEAD}
version=$(./getVersion.sh)

image_name=bfincher/html_browser:alpine-sqlite_$version

docker build --build-arg BRANCH=$branch_name -t $image_name .
