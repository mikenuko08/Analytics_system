echo "Provision student_vm"
echo "Step1: Update yum repository"
sudo yum -y update

echo "Step2: Add epel repository"
sudo yum -y epel-release

echo "Step3: Install necessary software"
sudo yum -y install gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker rsync lsyncd

echo "Step3: Install git (version >=2.4.0)"
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.4.0.tar.gz
tar -zxvf git-2.4.0.tar.gz
sudo mv git-2.4.0/ /
rm -rf git-2.4.0.tar.gz
cd /git-2.4.0
sudo ./configure --prefix=/usr/local
make
sudo make install
git -version

echo "Step4: Git setting"
#sudo mkdir /git
#sudo git -C /git init
sudo git config --global user.email "you@example.com"
sudo git config --global user.name "Your Name"
#sudo cp ~/git-commit.sh /git/
# 
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

echo "Step5: Script command setting"
sudo mkdir /var/log/script/
sudo chmod 777 /var/log/script
sudo cp /src/scriptlog.sh /etc/profile.d/
sudo chmod 644 /etc/profile.d/scriptlog.sh
sudo cp /src/lsyncd.conf /etc/lsyncd.conf

# sudo service lsyncd start