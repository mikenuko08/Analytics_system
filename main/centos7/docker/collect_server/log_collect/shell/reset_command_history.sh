#!/bin/bash
SCRIPT_DIR=`dirname $0`
while read row;
do
ipaddress=`echo ${row} | cut -d , -f 2`
if [ ${ipaddress} != "ip_address" ]; then
echo ${ipaddress}
ssh -t -t root@${ipaddress} << EOF
sudo rm -rf /var/log/script/*
exit
EOF
ssh -t -t logger@${ipaddress} << EOF
sudo rm -rf /root/.command_history
sudo touch /root/.command_history
exit
EOF
fi
done < /root/src2/log_collect/ip_address.csv
