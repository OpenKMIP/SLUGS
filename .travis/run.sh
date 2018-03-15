#!/bin/bash

set -e
set -x

if [[ "${RUN_INTEGRATION_TESTS}" == "1" ]]; then
    sudo mkdir -p /etc/slugs
    sudo cp ./.travis/slugs.conf /etc/slugs/slugs.conf
    sudo cp ./.travis/user_group_mapping.csv /etc/slugs/user_group_mapping.csv
    sudo mkdir -p /var/log/cherrypy/slugs
    sudo chmod 777 /var/log/cherrypy/slugs
    slugs -c /etc/slugs/slugs.conf &
    tox -r -e integration -- --url http://127.0.0.1:8080/slugs
else
    tox
fi
