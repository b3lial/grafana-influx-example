#!/bin/bash
set -e

if [ -z $1 ]; then
    echo "provide new grafana password via commandline parameter"
    exit 1
fi

docker volume create grafana-storage
docker run -d -p 3000:3000 \
	--name=grafana \
	-v grafana-storage:/var/lib/grafana \
	grafana/grafana

until [ "`docker inspect -f {{.State.Running}} grafana`"=="true" ]; do
    sleep 0.1;
done;

docker exec -it grafana grafana-cli --homepath "/usr/share/grafana" admin reset-admin-password $1