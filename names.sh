#!/bin/bash

if [ -n "$*" ]; then
  echo $@ | egrep -o --color=never '[0-9]{2}-[^/]*'
else
  find . -mindepth 1 -maxdepth 1 -type d | egrep -o --color=never '[0-9]{2}-[^/]*'
fi
