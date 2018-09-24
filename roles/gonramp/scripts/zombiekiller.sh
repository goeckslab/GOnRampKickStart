#!/usr/bin/env bash

Z=$(netstat -tulpn | grep ":40000" | awk '{print $7}' | sed 's|/.*||g')

echo "kill -9 $Z"

sleep 2

Z=$(netstat -tulpn | grep ":40000" | awk '{print $7}' | sed 's|/.*||g')

if ! [ -z "$Z" ]; then
  echo "More zombies!"
else
  echo "Zombielessness!"
fi
