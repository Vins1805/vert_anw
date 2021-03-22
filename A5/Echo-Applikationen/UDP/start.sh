#!/bin/sh
while :
do
  echo Server starting
  python echoServerUDP.py
  echo Hello World
done
exit /b 0