#!/bin/bash

# copy and enable lcd site api virtual server
cp ./dist/lcdmarket /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/lcdmarket /etc/nginx/sites-enabled/lcdmarket

# in development mode
if [ "$APP_IN_PRODUCTION" != "true" ]; then
    # migrations are automatic
    python3 /var/www/manage.py migrate --noinput
    # static files are collected on container init
    python3 /var/www/manage.py collectstatic --noinput
fi

exit 0
