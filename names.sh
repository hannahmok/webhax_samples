#!/bin/bash

find . -mindepth 1 -maxdepth 1 -type d | cut -c 3- | egrep --color=never '^[0-9]{2}-'
