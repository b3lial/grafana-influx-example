import os
import json
import logging
import sys
import requests

grafana_host = "osiris"
grafana_port = 3000
grafana_user = "admin"
grafana_password = "admin"
grafana_datasource = "InfluxDB"

influx_host = "osiris"
influx_port = 8086
influx_bucket = "cloudsensor"
influx_organisation = "phobosys"
influx_token = "O76lfizLy8f6DDeDZhRSIK4C49kYhKJtlbdgtOBPtQzTuuZmQ2kla7RKXLEhJ5GkFMLAD6C9GL2uaAbZF6vr8w=="


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
        logging.error("login response status %d", login_post.status_code)
        sys.exit()
    logging.info("login successful")

    # Add new datasource
    datasources_post = session.post(
        os.path.join(grafana_url, 'api', 'datasources'),
        data=json.dumps({
            'access': 'proxy',
            'database': '',
            'name': f'{grafana_datasource}',
            'type': 'influxdb',
            'basicAuth': True,
            'isDefault': True,
            'url': f'http://{influx_host}:{influx_port}',
            'user': '',
            'basicAuth': False,
            'basicAuthUser': '',
            'basicAuthPassword': '',
            'withCredentials': False,
            'jsonData': {
                'defaultBucket': f'{influx_bucket}',
                'httpMode': 'POST',
                'organization': f'{influx_organisation}',
                'version': 'Flux',
            },
            'secureJsonData': {
                'token': f'{influx_token}'
            }}),
        headers={'content-type': 'application/json'})
    if datasources_post.status_code != 200:
        logging.error("login response status %d", datasources_post.status_code)
        logging.error("login response test %s", datasources_post.text)
        sys.exit()
    logging.info("created new data source %s", grafana_datasource)

if __name__=="__main__":
    main()
