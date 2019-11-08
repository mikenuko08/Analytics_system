# change directory
cd /root/

# git install
yum install -y wget gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker autoconf python36*
sudo wget https://www.kernel.org/pub/software/scm/git/git-2.9.5.tar.gz
sudo tar vfx git-2.9.5.tar.gz;cd git-2.9.5;make configure;./configure --prefix=/usr/local;make all;make prefix=/usr/local install
# sudo visudoコマンドでsource_pathに/usr/local/bin/を追記
# 時間があれば，sedコマンドでできるようにする．

# histroy.shの配置
sudo cp ./history.sh /etc/profile.d/
sudo chmod 644 /etc/profile.d/history.sh
sudo cp ./.bashrc /root/

# script command setting
sudo mkdir -p /var/log/script/
sudo chmod 773 /var/log/script
sudo cp ./script.sh /etc/profile.d/
sudo chmod 644 /etc/profile.d/script.sh

# lsyncd install
sudo yum -y install epel-release
sudo sed -i -e "s/enabled=1/enabled=0/" /etc/yum.repos.d/epel.repo
sudo yum --enablerepo=epel install -y lsyncd
sudo cp ./lsyncd.conf /etc/
sudo mkdir -p /etc/lsyncd_exclude
sudo cp ./lsyncd_exclude/*.list /etc/lsyncd_exclude/
sudo mkdir -p /var/log/lsyncd
sudo systemctl enable lsyncd.service

# git setting
sudo mkdir /git
sudo /usr/local/bin/git -C /git init
sudo /usr/local/bin/git -C /git config user.name staff
sudo /usr/local/bin/git -C /git config user.email staff@softiv.info

sudo cp ./git-commit.sh /git/git-commit.sh
sudo chmod 755 /git/git-commit.sh

sudo cp ./init.sh /usr/local/bin/init.sh
sudo chmod u+x /usr/local/bin/init.sh

sudo cp ./ace /usr/local/bin/ace
sudo chmod 755 /usr/local/bin/ace