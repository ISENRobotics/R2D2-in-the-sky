#!/bin/bash
echo BB-UART1 > /sys/devices/bone_capemgr.*/slots
echo BB-UART2 > /sys/devices/bone_capemgr.*/slots
echo BB-UART4 > /sys/devices/bone_capemgr.*/slots

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
