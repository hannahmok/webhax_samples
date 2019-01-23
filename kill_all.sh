#!/bin/bash

for name in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3-); do
  docker kill demo-$name
done
