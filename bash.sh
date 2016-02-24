#!/bin/bash

if [ ps up `cat /tmp/mydaemon.pid ` >/dev/null ]
  then
    echo "Python process already running" >> /var/log/application.log
else
    /usr/bin/python /home/debian/robot.py
fi
