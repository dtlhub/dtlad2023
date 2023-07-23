#!/bin/sh

while true; do
    date -uR

    find "/tmp/data/" \
        -type d \
        -and -not -path "/tmp/data/" \
        -and -not -newermt "-900 seconds" \
        -exec rm -r {} +

    sleep 60
done
