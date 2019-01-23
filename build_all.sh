#!/bin/bash

for name in $(./names.sh); do
  pushd $name
  docker build -t demo/$name .
  popd
done
