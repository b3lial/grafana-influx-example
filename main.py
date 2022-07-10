import os
import json
import logging
import sys
import requests

grafana_host = "osiris"
grafana_port = 3000
grafana_user = "admin"
grafana_password = "admin"

ifdb_database = ""
datasource_name = ""
ifdb_password = ""
ifdb_host = ""
ifdb_port = 8086
ifdb_user = ""


def main():
    logging.basicConfig(level=logging.DEBUG)

    # login and open session
    logging.info("trying to login into grafana")
    grafana_url = os.path.join('http://', f'{grafana_host}:{grafana_port}')
    session = requests.Session()
    login_post = session.post(
        os.path.join(grafana_url, 'login'),
        data=json.dumps({
            'user': grafana_user,
            'email': '',
            'password': grafana_password }),
        headers={'content-type': 'application/json'})

    if login_post.status_code != 200:
        logging.error("login response %d, aborting", login_post.status_code)
        sys.exit()

    # Get list of datasources
    datasources_get = session.get(os.path.join(grafana_url, 'api', 'datasources'))
    datasources = datasources_get.json()
    logging.info("grafana server data sources: %s", datasources)

    # Add new datasource
    datasources_post = session.post(
        os.path.join(grafana_url, 'api', 'datasources'),
        data=json.dumps({
            'access': 'proxy',
            'database': '',
            'name': 'InfluxDB4',
            'type': 'influxdb',
            'basicAuth': True,
            'isDefault': True,
            'url': 'http://osiris:8086',
            'user': '',
            "basicAuth": False,
            'basicAuthUser': '',
            "basicAuthPassword": '',
            'withCredentials': False,
            'jsonData': {
                'defaultBucket': 'cloudsensor',
                'httpMode': 'POST',
                'organization': 'phobosys',
                'version': 'Flux',
            },
            'secureJsonData': {
                'token': 'O76lfizLy8f6DDeDZhRSIK4C49kYhKJtlbdgtOBPtQzTuuZmQ2kla7RKXLEhJ5GkFMLAD6C9GL2uaAbZF6vr8w=='
            }}),
        headers={'content-type': 'application/json'})
    if datasources_post.status_code != 200:
        logging.error("login response %d, aborting", datasources_post.status_code)
        logging.error("login response %s, aborting", datasources_post.text)
        sys.exit()

if __name__=="__main__":
    main()
