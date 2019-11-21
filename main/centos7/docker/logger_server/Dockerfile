FROM centos:7

# update yum package
RUN yum update -y

# change UTC to JST
RUN ln -sf  /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# install ssh and rsys
RUN yum install -y openssh-server rsyslog
RUN sed -i -e "s/#MaxStartups 10:30:100/MaxStartups 10:30:100/g" /etc/ssh/sshd_config
RUN sed -i -e "s/PasswordAuthentication yes/PasswordAuthentication no/g" /etc/ssh/sshd_config
RUN sed -i -e "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config
RUN echo "NETWORKING=yes" > /etc/sysconfig/network

# histroy.shの配置
COPY ./command/history.sh /etc/profile.d/
RUN chmod 644 /etc/profile.d/history.sh
COPY ./command/.bashrc /root/

# script command setting
RUN mkdir -p /var/log/script/
RUN chmod 773 /var/log/script
COPY ./command/script.sh /etc/profile.d/
RUN chmod 644 /etc/profile.d/script.sh

# change directory
WORKDIR /

# git install
RUN yum -y install gcc curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker autoconf wget make which iproute sudo
RUN wget https://www.kernel.org/pub/software/scm/git/git-2.9.5.tar.gz
RUN tar vfx git-2.9.5.tar.gz;cd git-2.9.5;make configure;./configure --prefix=/usr/local;make all;make prefix=/usr/local install
RUN rm git-2.9.5.tar.gz

# lsyncd install
RUN yum install -y epel-release
RUN sed -i -e "s/enabled=1/enabled=0/" /etc/yum.repos.d/epel.repo
RUN yum --enablerepo=epel install -y lsyncd
RUN yum remove -y epel-release
COPY ./file_edit/lsyncd/lsyncd.conf /etc/
RUN mkdir -p /etc/lsyncd_exclude
COPY ./file_edit/lsyncd/lsyncd_exclude/*.list /etc/lsyncd_exclude/
RUN mkdir -p /var/log/lsyncd


# git setting
RUN mkdir /git
RUN /usr/local/bin/git -C /git init
RUN /usr/local/bin/git -C /git config user.name staff
RUN /usr/local/bin/git -C /git config user.email staff@softiv.info

COPY ./file_edit/git-commit.sh /git/git-commit.sh
RUN chmod 755 /git/git-commit.sh

RUN echo "export LANG=ja_JP.UTF-8" > /etc/profile.d/setlang.sh
RUN chmod 644 /etc/profile.d/setlang.sh

COPY ./init.sh /usr/local/bin/init.sh
RUN chmod u+x /usr/local/bin/init.sh

COPY ./ace /usr/local/bin/ace
RUN chmod 755 /usr/local/bin/ace

RUN yum -y reinstall glibc-common
RUN localedef -v -c -i ja_JP -f UTF-8 ja_JP.UTF-8; echo "";
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

#add ssh user
ADD ./keys/id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN chown root.root /root/.ssh/authorized_keys

#user settings
RUN groupadd students
RUN useradd -D -g students
#RUN sed -i -e "s/USERGROUPS_ENAB yes/USERGROUPS_ENAB no/g" /etc/login.defs
RUN sed -i -e "s/UMASK           077/UMASK           072/g" /etc/login.defs

# ARG USER="logger"
RUN useradd logger -m
RUN usermod -aG wheel logger
WORKDIR /home/logger/
RUN chgrp students ../logger
COPY ./keys/id_rsa.pub .ssh/authorized_keys
RUN chmod 644 .ssh/authorized_keys;chmod 700 .ssh
RUN chown -R logger.logger .ssh/
RUN sed -i -e 's/# %wheel\tALL=(ALL)\tNOPASSWD: ALL/%wheel\tALL=(ALL)\tNOPASSWD: ALL/' /etc/sudoers
RUN sed -i -e 's/%wheel\tALL=(ALL)\tALL/# %wheel\tALL=(ALL)\tALL/' /etc/sudoers
RUN visudo -c

WORKDIR /root/data/
RUN cp -a /var/log/ /root/data/
RUN cp -a /home/ /root/data/
RUN cp -a /git/ /root/data/

CMD ["/usr/local/bin/init.sh"]
#CMD ["/sbin/init"]