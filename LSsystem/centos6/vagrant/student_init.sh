
sudo yum update -y

#sshd setting
sudo sed -i -e "s/#MaxStartups 10:30:100/MaxStartups 10:30:100/g" /etc/ssh/sshd_config
# sudo sed -i -e "s/PasswordAuthentication yes/PasswordAuthentication no/g" /etc/ssh/sshd_config
sudo sed -i -e "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config
sudo echo "NETWORKING=yes" > /etc/sysconfig/network

#add ssh user
sudo cp /vagrant/src/student/id_rsa /root/.ssh/authorized_keys
sudo chmod 600 /root/.ssh/authorized_keys
sudo chown root.root /root/.ssh/authorized_keys


useradd user1 -m
cd /home/user1/
cp /vagrant/src/student/id_rsa .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chown user1.user1 .ssh/authorized_keys

sudo cp /vagrant/src/student/history.sh /etc/profile.d/

# script command setting
sudo mkdir /var/log/script/
sudo chmod 773 /var/log/script
sudo cp /vagrant/src/student/script.sh /etc/profile.d/
sudo chmod 644 /etc/profile.d/script.sh

cd /root/
# git install
yum install -y wget gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker
wget https://www.kernel.org/pub/software/scm/git/git-2.2.0.tar.gz && tar -zxf git-2.2.0.tar.gz && cd git-2.2.0 && make prefix=/usr/local all && make prefix=/usr/local install

# lsyncd setting
wget ftp://ftp.riken.jp/Linux/fedora/epel/6/x86_64/Packages/e/epel-release-6-8.noarch.rpm
rpm -ivh ./epel-release-6-8.noarch.rpm
yum install --enablerepo=epel lsyncd -y
./lsyncd.conf /etc/lsyncd.conf

# git setting
mkdir /git
git -C /git init
git -C /git config user.name staff
git -C /git config user.email staff@softiv.info

sudo cp /vagrant/src/student/git-commit.sh /git/git-commit.sh
sudo chmod 755 /git/git-commit.sh

sudo cp /vagrant/src/student/history.sh /etc/profile.d/
sudo chmod 644 /etc/profile.d/history.sh

sudo cp /vagrant/src/student/init.sh /usr/local/bin/init.sh
sudo chmod u+x /usr/local/bin/init.sh

sudo cp /vagrant/src/student/ace /usr/local/bin/ace
sudo chmod 755 /usr/local/bin/ace

sudo cd /root/data/
sudo cp -a /var/log/ /root/data/
sudo cp -a /home/ /root/data/
sudo cp -a /git/ /root/data/

# 現状は以下のコマンドでgitbucketからリポジトリをクローン
#  GIT_SSH_COMMANDはsshの秘密鍵のディレクトリを直接指定するため
#  のオプション
# 
# sudo GIT_SSH_COMMAND="ssh -i /home/vagrant/.ssh/id_rsa -F &
# /dev/null" git clone ssh://git@192.168.0.8:29418/root/ & 
# edit_log.git /git
#
# pushする場合も同様に
#
# sudo GIT_SSH_COMMAND="ssh -i /home/vagrant/.ssh/id_rsa -F &
# /dev/null" git push origin master
# 