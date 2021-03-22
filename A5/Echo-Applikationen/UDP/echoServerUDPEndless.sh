#!/bin/sh
while :
do
  echo Server starting
  python echoServerUDP.py
  pause
done
exit /b 0
