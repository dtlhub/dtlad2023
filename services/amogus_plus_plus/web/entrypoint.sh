#!/bin/sh

chmod -R 777 /data

su - node -c "node /app/build"
