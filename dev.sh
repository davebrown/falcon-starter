#!/bin/bash

export DB_SERVER='something.database.windows.net'
export DB_NAME='testDB'
export DB_USER='ro_user'
export DB_PASSWORD=''

gunicorn --error-logfile - --log-file - --log-level debug \
         service:api
