# 評価実験用演習課題

## 演習概要

- ### 今回の演習課題を通して，3 種類の Web アプリケーションのデプロイを行う．演習の流れとしては，まず Web サーバである Apache のセットアップを行い各アプリケーションを動作させる為の環境の設定，アプリケーションのデプロイを行うという流れになっている．

- ### 演習時間は 100 分

## 実験の目的

- ### 今回の評価実験の目的として，サーバ管理演習を通して被験者が課題に行き詰まった際に，それを研究で作成したシステムが検知できるのかどうかという部分が重要になる． その為，課題に行き詰まった場合はすぐに教員または，西村に質問をしてください．

# Exercise1 　 Apache のセットアップ

## 1. Apache のインストール

### 実験環境は CentOS7 で動作しており、yum コマンドを利用してソフトのインストールや削除などを行う．yum コマンドの基本的な利用方法を以下に示す． Apache は httpd というソフトウェア名になっている．

### ソフトをインストールするコマンド

    yum -y isntall インストールしたいソフトウェア名

### インストールしたソフトを確認するコマンド

    yum list

### パッケージ量が非常に多いため，grep 等を用いて絞り込む必要がある．

###

## 2. Apache の操作方法

### インストールが完了したら Apache を起動するコマンドを実行する．また以下に Apache の動作に関する操作方法を記している．設定ファイルを編集した場合は再起動を行う必要がある．必要に応じて以下のコマンドを参考にしてほしい．

### 起動

    systemclt start ソフトウェア名

### 停止

    systemctl stop ソフトウェア名

### 再起動

    systemctl restart ソフトウェア名

### 状態確認

    systemctl status ソフトウェア名

### ここままの設定であれば,PC をシャットダウンすると OS の全てのプロセスが終了してしまうため，PC を起動するたびに起動のコマンドを実行する必要がある.そこを省略する為に,以下のコマンドが用意されている.自動起動の設定を実行

自動起動設定

    systemctl enable ソフトウェア名

自動起動解除

    systemctl disable ソフトウェア名

## 3. 動作確認方法

### 以下のコマンドを実行して， Apache のサンプルページの HTML が取得できれば正しく動作していることが確認できる．

    curl http://localhost/

### または，ブラウザで以下の URL にアクセスする

    http://localhost/

# Exercise2 　 Gitbucket

## 1. Java のインストール

### Gitbucket は Java Servlet という仕組みで動作している．従って，この環境で Java が動作する必要がある．以下のコマンドを実行すると Java をインストールできる．

    yum -y install java-1.8.0-openjdk-devel.x86_64

## 1. Tomcat のセットアップ

### Gitbucket を動作させるためには，Tomcat と呼ばれる Java Servlet を実行するソフトウェアが必要になる．そこで以下のコマンドにより Tomcat 本体とサンプルページをインストールする．

### Tomcat と Tomcat のサンプルページのインストール

    yum -y install tomcat tomcat-webapps

### 続けて，以下のコマンドも実行する．

### Tomcat の起動方法

    systemctl start tomcat

### Tomcat の自動起動設定方法

    systemctl enable tomcat

### 以下のコマンドを実行して， Tomcat のサンプルページの HTML が取得できれば正しく動作していることが確認できる．

    curl localhost:8080

## 2. gitbucket のファイルをダウンロードする

### gitbucket のファイルをダウンロードする前にファイルを配置するためのディレクトリに移動してもらう. 配置先のディレクトリは、/var/lib/tomcat/webapps/である.

### インターネットからソフトをダウンロードする際に利用できるコマンドとして代表的なものに wget がある. 以下に基本的な使い方を示す.

    wget ダウンロードしたいファイルのURL

### 今回構築したい gitbucket のファイルは以下の URL にある

https://github.com/gitbucket/gitbucket/releases/download/4.8/gitbucket.war

## 3. リバースプロキシの設定を行う(Apache と Tomcat の連携設定)

    echo "ProxyPass / ajp://localhost:8009/" > /etc/httpd/conf.d/proxy.conf
    systemctl restart httpd

# Exercise3 　 pukiwiki

## 1. PHP のセットアップ

### pukiwiki は PHP で動作しているソフトウェアである．

### pukiwiki は PHP で動作している．従って，この環境で PHP が動作する必要がある．以下のコマンドを実行すると PHP をインストールできる．

    yum -y install php php-mbstring

## 2. PHP の設定ファイルをコピーしておく

    cd /etc
    cp php.ini php.ini.org

## 3. PHP の設定ファイルを編集する

    vi php.ini
    date.timezone = Asia/Tokyo

## 4. PHP の設定を読み込ませるために，Apache の再起動を行う．

    systemclt restart httpd

## 5.

    cd /var/www/html
    wget "https://ja.osdn.net/frs/redir.php?m=iij&f=pukiwiki%2F69652%2Fpukiwiki-1.5.2_utf8.zip" -O pukiwiki.zip

##

    // yum -y install unzip
    unzip pukiwiki.zip
    mv pukiwiki-1.5.2_utf8 pukiwiki
    rm -rf pukiwiki.zip

##

    chown apache:apache pukiwiki

# Exercise3 　 GROUP SESSION
