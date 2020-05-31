#!/bin/bash

version=$(cat version.txt)
docker push bfincher/html_browser:alpine-sqlite_$version  
docker push bfincher/html_browser:alpine-sqlite_latest
docker push bfincher/html_browser:alpine-mysql_$version  
docker push bfincher/html_browser:alpine-mysql_latest
