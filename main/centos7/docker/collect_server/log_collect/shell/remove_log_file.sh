#!/bin/bash
TARGET=root
USER=logger
SCRIPT_DIR=`dirname $0`
while read host;
do
ipaddress=`echo ${host} | cut -d , -f 2`
if [ ${ipaddress} != "ip_address" ]; then
echo ${ipaddress}
ssh -t -t $TARGET@${ipaddress} << EOF
exit
EOF
ssh -t -t $USER@${ipaddress} << EOF
echo '---- delete script file ----'
sudo ls -la /var/log/script/*
sudo rm -rf /var/log/script/*
sudo ls -la /var/log/script/*
echo '---------- finish ----------'
echo ''
echo '--- delete history file ---'
sudo ls -la /$TARGET/.command_history
sudo cat /$TARGET/.command_history
sudo rm -rf /$TARGET/.command_history
sudo ls -la /$TARGET/.command_history
sudo cat /$TARGET/.command_history
echo '--------- finish ---------'
exit
EOF
fi
done < /root/log_collect/main/ip_address.csv
