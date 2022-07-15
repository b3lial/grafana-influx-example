import os
import json
import logging
import sys
import requests

GRAFANA_PORT = 3000
GRAFANA_DATASOURCE = "InfluxDB"
INFLUX_PORT = 8086


def main():
    logging.basicConfig(level=logging.DEBUG)

    # parse commandline
    argumentList = sys.argv[1:]
    n = len(argumentList)
    if n != 7:
        logging.error("expected 7 commandline parameters")
        sys.exit(os.EX_SOFTWARE)

    grafana_user = argumentList[0]
    grafana_password = argumentList[1]
    grafana_host = argumentList[2]
    influx_token = argumentList[3]
    influx_host = argumentList[4]
    influx_bucket = argumentList[5]
    influx_organisation = argumentList[6]

    # login and open session
    logging.info("trying to login into grafana")
    grafana_url = os.path.join('http://', f'{grafana_host}:{GRAFANA_PORT}')
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
        sys.exit(os.EX_SOFTWARE)
    logging.info("login successful")

    # Add new datasource
    datasources_post = session.post(
        os.path.join(grafana_url, 'api', 'datasources'),
        data=json.dumps({
            'access': 'proxy',
            'database': '',
            'name': f'{GRAFANA_DATASOURCE}',
            'type': 'influxdb',
            'isDefault': True,
            'url': f'http://{influx_host}:{INFLUX_PORT}',
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
        sys.exit(os.EX_SOFTWARE)
    logging.info("created new data source %s", GRAFANA_DATASOURCE)

if __name__=="__main__":
    main()
