#!/usr/bin/env bash

BBTMP="/tmp/gonramp/bbtmp"
BB="/tmp/gonramp/bioblend"

if [ -d $BB ]; then
  exit
fi

BBGH="https://github.com/galaxyproject/bioblend.git"
VERSION="v0.10.0"

git clone --depth 1 -b $VERSION $BBGH $BBTMP
cp -r $BBTMP/bioblend $BB
rm -rf $BBTMP
