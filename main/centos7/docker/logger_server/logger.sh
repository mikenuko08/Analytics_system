# histroy.shの配置
cp ./command/history.sh /etc/profile.d/
chmod 644 /etc/profile.d/history.sh
cp ./command/.bashrc /root/

# script command setting
mkdir -p /var/log/script/
chmod 773 /var/log/script
cp ./command/script.sh /etc/profile.d/
chmod 644 /etc/profile.d/script.sh

# change directory
cd /

git install
yum -y install gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker autoconf wget make which iproute sudo
wget https://www.kernel.org/pub/software/scm/git/git-2.9.5.tar.gz
tar vfx git-2.9.5.tar.gz;cd git-2.9.5;make configure;./configure --prefix=/usr/local;make all;make prefix=/usr/local install
rm git-2.9.5.tar.gz

# lsyncd install
yum install -y epel-release
sed -i -e "s/enabled=1/enabled=0/" /etc/yum.repos.d/epel.repo
yum --enablerepo=epel install -y lsyncd
yum remove -y epel-release
cp ./file_edit/lsyncd/lsyncd.conf /etc/
mkdir -p /etc/lsyncd_exclude
cp ./file_edit/lsyncd/lsyncd_exclude/*.list /etc/lsyncd_exclude/
mkdir -p /var/log/lsyncd

# git setting
mkdir /git
/usr/local/bin/git -C /git init
/usr/local/bin/git -C /git config user.name staff
/usr/local/bin/git -C /git config user.email staff@softiv.info

cp ./file_edit/git-commit.sh /git/
cp ./file_edit/.gitignore /git/
chmod 755 /git/git-commit.sh

#add ssh user
cp ./keys/id_rsa.pub /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
chown root.root /root/.ssh/authorized_keys

#user settings
groupadd students
useradd -D -g students
#sed -i -e "s/USERGROUPS_ENAB yes/USERGROUPS_ENAB no/g" /etc/login.defs
sed -i -e "s/UMASK           077/UMASK           072/g" /etc/login.defs

# logger user settings
useradd logger -m
usermod -aG wheel logger
cd /home/logger/
chgrp students ../logger
cp ./keys/id_rsa.pub .ssh/authorized_keys
chmod 644 .ssh/authorized_keys;chmod 700 .ssh
chown -R logger.logger /var/log/script
chown -R logger.logger .ssh/
# add sudo user
sed -i -e 's/# %wheel\tALL=(ALL)\tNOPASSWD: ALL/%wheel\tALL=(ALL)\tNOPASSWD: ALL/' /etc/sudoers
sed -i -e 's/%wheel\tALL=(ALL)\tALL/# %wheel\tALL=(ALL)\tALL/' /etc/sudoers
visudo -c