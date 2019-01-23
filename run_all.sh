#!/bin/bash

for name in $(./names.sh $@); do
  docker run --rm -d -p 99$(cut -c -2 <<<$name):80 --name demo-$name demo/$name
done
