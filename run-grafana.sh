#!/bin/bash
set -e

GF_PASSWD=admin2

docker volume create grafana-storage
docker run -d -p 3000:3000 \
	--name=grafana \
	-v grafana-storage:/var/lib/grafana \
	grafana/grafana
sleep 1
docker exec -it grafana grafana-cli --homepath "/usr/share/grafana" admin reset-admin-password $GF_PASSWD