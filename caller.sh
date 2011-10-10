#!/bin/bash
while true
do
  python bighands.py -t pdf -a 100 -r -o "/var/www/hail_katrina/baby_crawler/"&
  pid=$!
  sleep 300
done

