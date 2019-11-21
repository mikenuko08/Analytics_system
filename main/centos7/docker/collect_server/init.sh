#!/bin/sh

first(){
    echo "The following procedure is invoked only once"
    cp -a /root/data/log/ /var/
    cp -a /root/data/home/ /home/
    cp -a /root/data/git/ /git/
}
init(){
    echo "The following procedure is always invoked"
    echo "container start" >> /var/log/docker_container
    date >> /var/log/docker_container
}

if [ ! -r /var/log/docker_container ] ; then
    first
    # systemctl enable lsyncd
fi

init

cat <<EOF >>~/.bashrc
function TERMINATE {
    systemctl stop rsyslog
    systemctl stop sshd
    # systemctl stop lsyncd
    echo "container terminate" >> /var/log/docker_container
    date >> /var/log/docker_container
}
trap 'TERMINATE; exit 0' TERM
EOF
exec /sbin/init
