echo "Provision teacher_vm"
echo "Step1: Update yum repository"
sudo yum -y update

echo "Step2: Add epel-repository and ius-repository"
sudo yum -y install epel-release
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm

echo "Step3: Install necessary software"
sudo yum -y install java-1.8.0-openjdk-devel gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker python36*

echo "Step4: Install git (version >=2.2.0)"
# git install
yum install -y wget gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker
wget https://www.kernel.org/pub/software/scm/git/git-2.2.0.tar.gz && tar -zxf git-2.2.0.tar.gz && cd git-2.2.0 && make prefix=/usr/local all && make prefix=/usr/local install
# sudo visudoコマンドでsource_pathに/usr/local/bin/を追記
# 時間があれば，sedコマンドでできるようにする．

echo "Step5: Mongodb configuration"
# 以下は公式ページを参照 https://docs.mongodb.com/v3.4/tutorial/install-mongodb-on-amazon/
# Install MongoDB Community Edition
# 1. Configure the package management system (yum)
# sudo vim /etc/yum.repos.d/mongodb-org-3.4.repo
# ----------------
# [mongodb-org-3.4]
# name=MongoDB Repository
# baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.4/x86_64/
# gpgcheck=1
# enabled=1
# gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc
# ----------------
# 
sudo cp /vagrant/src/teacher/mongodb-org-3.4.repo /etc/yum.repos.d/

# 2. Install the MongoDB packages and associated tools.
sudo yum install -y mongodb-org
# 
# Run MongoDB Community Edition
# 1. Start MongoDB
sudo systemctl enable mongod.service 
# 2. Verify that MongoDB has started successfully
# 3. Stop MongoDB
# sudo service mongodb stop
# 4. Restart MongoDB
# sudo service mongodb restart
# sudo chkconfig mongod on

echo "Step6: Apache configuration"
sudo yum -y install httpd
sudo systemctl start httpd.service
# sudo chkconfig httpd on
sudo systemctl status httpd.service

echo "Step7: Tomcat7 configuration"
sudo yum -y install tomcat tomcat-webapps
sudo systemctl tomcat.service start
# sudo chkconfig tomcat on
sudo systemctl status tomcat.service

echo "Step8: Link Apache and Tomcat7"
echo "Please execute the following command"
# Apache側の設定
# 1. 以下の設定が含まれていることを確認
# cat /etc/httpd/conf.modules.d/00-proxy.conf
# ----------------
# LoadModule proxy_module modules/mod_proxy.so
# LoadModule proxy_ajp_module modules/mod_proxy_ajp.so
# ----------------
# 
# 2. 以下のファイルを作成
# sudo vim /etc/httpd/conf.d/proxy-ajp.conf
# <Location / >
#  ProxyPass ajp://localhost:8009/
#  Order allow,deny
#  Allow from all
# </Location>
#
# Tomcat側の設定
# 3. 以下の設定が含まれていることを確認
# cat /etc/tomcat/server.xml
# ----------------
# <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
# ----------------
# ----------------
# Apache側からTomcatのページを表示させるため、8080ポートの設定を無効化する。
# <!--
# <Connector port="8080" protocol="HTTP/1.1"
#  connectionTimeout="20000"
#  redirectPort="8443" />
# -->
# ----------------
# 
# 4. Apacheの再起動
# sudo service httpd restart

echo "Step9: Gitbucket configuration"
sudo wget https://github.com/gitbucket/gitbucket/releases/download/4.21.0/gitbucket.war
sudo mv gitbucket.war /var/lib/tomcat/webapps/
# gitbucketの設定ファイルも時間があれば自動化する
# 下記のファイルをsedコマンドで編集すれば，base_urlとSSH，SSH用のhostの登録は可能
# sudo vim /usr/share/tomcat/.gitbucket/gitbucket.conf
# sshの公開鍵の登録がコマンドから行えるかが現状わからないため，
# とりあえず，手動で設定する．

echo "Step10: Python3 configuration"
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
sudo ln -s /usr/bin/pip3.6 /usr/bin/pip3
sudo pip3 install fabric
sudo pip3 install pandas
sudo pip3 install flask
sudo pip3 install flask-bootstrap
sudo pip3 install flask-pymongo
sudo pip3 install python-dateutil

