#!/bin/bash

for name in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3-); do
  pushd $name
  docker build -t demo/$name .
  popd
done
