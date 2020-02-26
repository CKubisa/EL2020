#!/bin/bash

#Sees if website in online
site="$1"

wget -q --spider $site

if [ $? -eq 0 ]; then
    echo "is online"
else
    echo "is ofline"
fi
