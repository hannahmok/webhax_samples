#!/bin/bash

for name in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3-); do
  docker run --rm -d -p 99$(cut -c -2 <<<$name):80 --name demo-$name demo/$name
done
