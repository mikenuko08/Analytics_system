# yum package update
yum update -y

# history command setting
scp ~/history.sh /etc/profile.d/

# script command setting
mkdir /var/log/script/
chmod 773 /var/log/script
scp ~/script.sh /etc/profile.d/
chmod 644 /etc/profile.d/script.sh

cd /root/
# git install
yum install -y wget gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker
wget https://www.kernel.org/pub/software/scm/git/git-2.2.0.tar.gz && tar -zxf git-2.2.0.tar.gz && cd git-2.2.0 && make prefix=/usr/local all && make prefix=/usr/local install

# lsyncd setting
wget ftp://ftp.riken.jp/Linux/fedora/epel/6/x86_64/Packages/e/epel-release-6-8.noarch.rpm
rpm -ivh ./epel-release-6-8.noarch.rpm
yum install --enablerepo=epel lsyncd -y
rm -rf epel-release-6-8.noarch.rpm
scp ./lsyncd.conf /etc/lsyncd.conf

# git setting
mkdir /git
git -C /git init
git -C /git config user.name staff
git -C /git config user.email staff@softiv.info

scp ~/git-commit.sh /git/git-commit.sh
chmod 755 /git/git-commit.sh

scp ~/history.sh /etc/profile.d/
chmod 644 /etc/profile.d/history.sh

scp ~/init.sh /usr/local/bin/init.sh
chmod u+x /usr/local/bin/init.sh

scp ~/ace /usr/local/bin/ace
chmod 755 /usr/local/bin/ace

cd /root/data/
cp -a /var/log/ /root/data/
cp -a /home/ /root/data/
cp -a /git/ /root/data/

# 現状は以下のコマンドでgitbucketからリポジトリをクローン
#  GIT_SSH_COMMANDはsshの秘密鍵のディレクトリを直接指定するため
#  のオプション
# 
# GIT_SSH_COMMAND="ssh -i /home/vagrant/.ssh/id_rsa -F &
# /dev/null" git clone ssh://git@192.168.0.8:29418/root/ & 
# edit_log.git /git
#
# pushする場合も同様に
#
# GIT_SSH_COMMAND="ssh -i /home/vagrant/.ssh/id_rsa -F &
# /dev/null" git push origin master
# 
