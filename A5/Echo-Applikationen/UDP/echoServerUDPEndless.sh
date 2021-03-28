#!/bin/bash
while :; do
  if [[ ! $(pgrep -f echoServerUDP.py) ]]; then
      echoServerUDP.py
  fi
done
