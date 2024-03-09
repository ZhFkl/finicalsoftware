#!/bin/bash

containerName='graphcube-server'
containerId=`docker ps -aq --filter name=$containerName`

if [[ -n $containerId ]]; then
    docker stop $containerId
    docker rm $containerId
fi

imageTag='graphcube-backend'
imageId=`docker images |grep -i $imageTag | head -1 |awk '{print $3}' `

if [[ -n $imageId ]]; then
    docker rmi $imageId
fi

docker build . -t $imageTag
docker run -d -p 9000:8000 --name $containerName $imageTag