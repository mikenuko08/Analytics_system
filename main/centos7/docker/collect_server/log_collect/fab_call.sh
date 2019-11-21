#! /bin/bash
while true; 
do
/home/log_collect/log_collect.sh > /dev/null; 
sleep 300; 
done &
