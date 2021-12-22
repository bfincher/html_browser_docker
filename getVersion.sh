#!/bin/bash

version=$(grep VERSION .env)
version=$(echo $version | awk -F'=' ' { print $2} ')
echo $version
