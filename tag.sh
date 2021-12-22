#!/bin/bash

version=$(./getVersion.sh)
docker tag bfincher/html_browser:alpine-sqlite_$version  bfincher/html_browser:alpine-sqlite_latest
docker tag bfincher/html_browser:alpine-mysql_$version  bfincher/html_browser:alpine-mysql_latest
