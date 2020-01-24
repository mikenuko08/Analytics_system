systemctl stop lsyncd
cd /git
ls
rm -rf .git/ etc/ root/ var/
ls
echo 'chrony*' >> /etc/lsyncd_exclude/etc.list
echo 'lib/chrony*' >> /etc/lsyncd_exclude/var.list
cd /git
git init
systemctl start lsyncd
