#!/bin/sh

# first(){
#     echo "The following procedure is invoked only once"
#     cp -a /root/data/log/ /var/
#     cp -a /root/data/home/ /
#     cp -a /root/data/git/ /
# }

init(){
    echo "The following procedure is always invoked"
    echo "container start" >> /var/log/container
    date >> /var/log/container
}

# if [ ! -r /var/log/container ] ; then
#     first
# fi

init

cat <<EOF >>~/.bashrc
function TERMINATE {
    sevice rsyslog stop
    sevice sshd stop
    sevice lsyncd stop
    echo "container terminate" >> /var/log/container
    date >> /var/log/container
}
trap 'TERMINATE; exit 0' TERM
EOF
exec /sbin/init
