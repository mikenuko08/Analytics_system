echo "Provision teacher_vm"
echo "Step1: Update yum repository"
sudo yum -y update

echo "Step2: Add epel repository"
sudo yum -y epel-release

echo "Step3: Install java8"
sudo yum -y install java-1.8.0-openjdk-devel
java --version

echo "Step4: Apache configuration"
sudo yum -y install httpd
sudo service httpd start
sudo chkconfig httpd on
sudo service httpd status

echo "Step5: Tomcat7 configuration"
sudo yum -y install tomcat tomcat-webapps
sudo service tomcat start
sudo chkconfig tomcat on
sudo service tomcat status

echo "Step6: Gitbucket configuration"
sudo wget https://github.com/gitbucket/gitbucket/releases/download/4.21.0/gitbucket.war
