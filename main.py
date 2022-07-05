import requests
import os
import json
import logging

grafana_host = "localhost"
grafana_port = 3000
grafana_user = "admin"
grafana_password = "admin"

ifdb_database = ""
datasource_name = ""
ifdb_password = ""
ifdb_host = ""
ifdb_port = ""
ifdb_user = ""

def main():
    logging.basicConfig(level=logging.DEBUG)

    # login and open session
    logging.info("trying to login into grafana")
    grafana_url = os.path.join('http://', '%s:%u' % (grafana_host, grafana_port))
    session = requests.Session()
    login_post = session.post(
        os.path.join(grafana_url, 'login'),
        data=json.dumps({
            'user': grafana_user,
            'email': '',
            'password': grafana_password }),
        headers={'content-type': 'application/json'})

    if login_post.status_code != 200:
        logging.error("login response {}, aborting".format(login_post.status_code))
        exit()

    # Get list of datasources
    datasources_get = session.get(os.path.join(grafana_url, 'api', 'datasources'))
    datasources = datasources_get.json()
    logging.info("grafana server data sources: {}".format(datasources))

    # Add new datasource
    datasources_put = session.put(
        os.path.join(grafana_url, 'api', 'datasources'),
        data=json.dumps({
            'access': 'direct',
            'database': ifdb_database,
            'name': datasource_name,
            'password': ifdb_password,
            'type': 'influxdb_08',
            'url': 'http://%s:%u' % (ifdb_host, ifdb_port),
            'user': ifdb_user}),
        headers={'content-type': 'application/json'})

if __name__=="__main__":
    main()