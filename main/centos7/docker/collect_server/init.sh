#!/bin/sh

first(){
    echo "The following procedure is invoked only once"
    cp -a /root/data/log/ /var/
    cp -a /root/data/git/ /git/
    #python3.6 configuration"
    #ln -s /usr/bin/python3.6 /usr/bin/python3
    #ln -s /usr/bin/pip3.6 /usr/bin/pip3
    mkdir ~/log
    pip3 install fabric
    pip3 install pandas
    pip3 install flask
    pip3 install flask-bootstrap
    pip3 install flask-pymongo
    pip3 install python-dateutil
    pip3 install python-dotenv
    pip3 install pyvirtualdisplay
    pip3 install GitPython
    pip3 install sklearn
    pip3 install selenium 
    pip3 install chromedriver-binary
}

init(){
    echo "The following procedure is always invoked"
    echo "container start" >> /var/log/docker_container
    date >> /var/log/docker_container
}

if [ ! -r /var/log/docker_container ] ; then
    first
    systemctl start crond
    systemctl enable crond
    # systemctl start lsyncd
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
