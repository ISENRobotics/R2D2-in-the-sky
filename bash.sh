#!/bin/bash

i="0"
while [ "$i" -lt 60 ]
do
  if [ ps up `cat /tmp/mydaemon.pid ` >/dev/null ]
    then
      echo "Python process already running" >> /var/log/application.log
  else
      /usr/bin/python /home/debian/robot.py
  fi
  i=$[$i+1]
  sleep 1
done
