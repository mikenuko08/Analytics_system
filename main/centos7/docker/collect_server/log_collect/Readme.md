# log_collect 以下にあるファイルの紹介

## ログ収集用プログラム(Python3)

### fabfile.py

サーバの状況を確認するコマンドを実行し，その結果を~/fabfile.log として記録するスクリプト

### log_backup.py

学生が編集したファイルを集約した/git と学生が実行したコマンドとその結果を.command.log と/script として取得する為のスクリプト
ログは，~/log_backup.log に記録される

### add_group_id.py

実行するごとにただひたすらに，group_num を増やし続けるだけのスクリプト

## 起動スクリプト

### log_collect.sh

fabfile.py と log_collect.py を実行し，結果をログファイル fabfile.log と log_backup.log に出力する．これにより，プログラムが正常に動作しているか確認できる．

### countup.sh

add_group_id.py を実行し，結果を countup.log に出力する．

### \*fab_call.sh

log_collect.sh を 5 分毎に実行するスクリプト．  
収集する学生の人数が多い場合 crontab では動かないことがある為，その際に利用する詳細は\*3 に記述．

### setup.sh

学生のログ収集環境設定後，history のログを正しく記録する為に，ログインとログアウトを行う．(仕様上,ログ収集環境を使用する前にこのスクリプトを実行する必要がある．)  
ex. setup.sh

```
ssh -t -t root@base_ipaddress << EOF
exit
EOF
```

## 必須な設定ファイル

### id_rsa.pub

先生の公開鍵

### group_num

授業が何周目なのかをこのファイルから読み出す

### iptable.csv

各学生の id とマシンの IP アドレスを対応づける．ここを編集するだけで，学生の人数を調節することができる

# 教員用ログ収集環境の起動方法

学生用ログ収集環境において以下の事を行った前提で，教員用ログ収集環境を起動すること．

0. 軸となる一台のマシンの中に sudo コマンドが実行できる logger ユーザを作成．
1. /src を/home/logger に配置する．
1. install.sh と rm.sh に実行権限を付与する.
1. install.sh を実行する.
1. 教員用のログ収集環境にログインし，setup.sh を実行する．
1. 教員に学生用ログ収集環境を指定台数(今回は 20 台)コピーしてもらう.

### 0. コピー終了後，教員用ログ収集環境にログインし，reset_command_history.sh を実行する．

```
cd src2/log_collect
chmod +x reset_command_history.sh
./reset_command_history.sh
```

### 1. ip_address.csv にログ収集を行うマシン(教員にコピーしてもらったマシンの IP アドレス)を登録

ex. ip_address.csv

```
student_id,ip_address
1,150.89.223.71
2,150.89.223.72
3,150.89.223.73
・
・
・
20,150.89.223.90
```

### 2. group_num に 0 を設定(二週間に一回加算する事により，何周目の学生か特定できる)

ex. group_num

```
0 〜 4or5
```

### 3. crontab に log_collect.sh と countup.sh を登録 (人数が多い場合これでは動作しないことがある\*3 へ)

ex. crontab -e

```
*/5 * * * * /root/src2/log_collect/log_collect.sh
00 10 * * * /root/src2/log_collect/countup.sh
```

### \*3-1. nohup コマンドを使って fab_call.sh を実行する

```
nohup /root/src2/log_collect/fab_call.sh &
```

### \*3-2. nohup コマンドを利用した場合 countup.sh は手動で実行する

```
./countup.sh
```

### 4. 動作確認を行う．

ログファイルがホームディレクトリ以下に出力されるようになっている．
・fabfile.log
・log_backup.log
・countup.log
上記を確認して，正常に動作していれば終了．
