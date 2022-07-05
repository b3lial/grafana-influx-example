import requests
import os
import json
import logging

grafana_host = "localhost"
grafana_port = 3000
grafana_user = "admin"
grafana_password = "admin"

def main():
    logging.basicConfig(level=logging.DEBUG)

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

if __name__=="__main__":
    main()