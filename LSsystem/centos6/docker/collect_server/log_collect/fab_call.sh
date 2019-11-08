#! /bin/bash
while true; 
do
/root/src2/log_collect/log_collect.sh > /dev/null; 
sleep 300; 
done &
