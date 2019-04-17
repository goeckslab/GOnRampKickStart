#!/usr/bin/env bash
MASQUERADE_ADDRESS="$(ip a | grep 192 | sed 's/.*inet //' | sed 's|/24.*||')"

if [ -z "$MASQUERADE_ADDRESS" ]; then
	MASQUERADE_ADDRESS="$(curl -s icanhazip.com)"
fi

if [ ! $? ]; then
	exit 1
fi

export MASQUERADE_ADDRESS

STR2="MASQUERADE_ADDRESS=\"$MASQUERADE_ADDRESS\""
if [ -z "$(cat /etc/environment | grep MASQUERADE_ADDRESS)" ]; then
  echo "$STR2" >> /etc/environment
else
  sudo sed -i "/MASQUERADE_ADDRESS/c\\$STR2" /etc/environment
fi
