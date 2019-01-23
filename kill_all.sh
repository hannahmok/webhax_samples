#!/bin/bash

for name in $(./names.sh $@); do
  docker kill demo-$name
done
