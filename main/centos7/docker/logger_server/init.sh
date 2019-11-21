#!/bin/sh

first(){
    echo "The following procedure is invoked only once"
    cp -a /root/data/log/ /var/
    cp -a /root/data/home/ /home/
    cp -a /root/data/git/ /git/
    touch /root/.bash_history
    touch /home/logger/.bash_history
}

init(){
    echo "The following procedure is always invoked"
    echo "container start" >> /var/log/container
    date >> /var/log/container
    
}

if [ ! -r /var/log/container ] ; then
    first
    systemctl enable lsyncd.service
fi

init

cat <<EOF >>~/.bashrc
function TERMINATE {
    systemctl stop rsyslog
    systemctl stop sshd
    systemctl stop lsyncd
    echo "container terminate" >> /var/log/container
    date >> /var/log/container
}
trap 'TERMINATE; exit 0' TERM
EOF
exec /sbin/init
