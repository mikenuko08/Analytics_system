- コメント付き鍵ファイルの作成
  - ssh-keygen -t RSA -C "@user1"

- ユーザ追加コマンド
  - useradd user1 -m

- id_rsa1~3が対象ユーザの秘密鍵．以下参照．
  - Dropbox\mkhr_research\igaki\sshkey

- root/user1/user2/user3のユーザが存在する．
  - rootはuser1の秘密鍵で，user1~3はそれぞれ対応する秘密鍵でログインできる．

- 実行方法
  - serverディレクトリを丸ごとどこかにコピー
  - serverディレクトリ内でdocker-compose build && docker-compose up -dと実行する
  - IP:2000 でログインできる

Herokuようにvolumesタグをdocker-compose.ymlから削除
    volumes:
      - ./data/log/:/var/log/
      - ./data/home/:/home/
      - ./data/git/:/git/
