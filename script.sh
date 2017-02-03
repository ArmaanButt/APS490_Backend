#!/bin/bash

host="$MYSQL_HOST"
port="3306"
user="$MYSQL_USER"
password="$MYSQL_PASSWORD"

while ! mysql -h"$host" -P"$port" -u"$user" -p"$password"  -e ";" ; do
    >&2 echo "Can't connect, please retry"
    sleep 1
done

>&2 echo "MYSQL is up - executing command"
python run.py
