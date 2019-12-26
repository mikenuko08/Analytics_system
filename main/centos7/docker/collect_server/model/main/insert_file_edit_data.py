import os
import sys
import glob
import pandas as pd
from mongo_connect import DBController
from git import *

import tarfile

# DB名/コレクション名
db_name = 'students'
db_col_fileEdit = 'file_edit'

# gitbacketのIPアドレス
gitbucket = '192.168.33.1'


# git.tar.gzファイルを展開する
def open_tarfile(file_path):
    # scriptコマンドで収集したscript.tar.gzを展開
    with tarfile.open(file_path, 'r:gz') as tf:
        # file_path[:-10]はgit.tar.gzまでのpathを意味している
        tf.extractall(file_path[:-10])


def insert_fileEdit_data(db_con_fileEdit, file_path, file_path_list):

    if(len(file_path_list) == 8):
        # studentID
        studentID = file_path_list[5]
        # unixtime
        unixtime_str = file_path_list[6]
        unixtime = int(unixtime_str)
        print(unixtime)

        # ファイル名
        file_name = file_path_list[7]
        print(file_name)

        ''' ファイル編集履歴のリモートへのpush手順
        tar -zxvf git.tar.gz && cd git
        git remote add origin ssh://git@192.168.33.1:29418/root/002.git
        * リモートリポジトリを削除する時はgit remote rm origin
        git pull origin master
        git push origin master
        '''
        open_tarfile(file_path)
        git_path = '/'.join(file_path_list[:7]) + '/git'
        git_remote_url = 'ssh://git@' + gitbucket + ':29418/root/' + studentID + '.git'
        print(git_path)
        os.chdir(git_path)
        os.system('git remote add origin ' + git_remote_url)
        os.system('git fetch')
        os.system('git push origin master')

        # GitPythonでも実装は可能かも？(テストする時間がないので省略)
        # repo = Repo(git_path)
        # origin = repo.create_remote('origin', git_remote_url)
        # origin.fetch()
        # origin.push()

        ''' ファイル編集履歴のコミット履歴をDBに追加する処理
        1. GitPythonを利用して、git logコマンドを実行.
        2. git logコマンドの結果(コミット時刻, コミットのハッシュ値, 変更されたファイル群の名称など)を変数に保持
        3. 変数に保持された結果をDBに追加処理する
        '''

        repo = Repo(git_path)
        for item in repo.iter_commits('master', max_count=100):
            print('================================')
            print(item.hexsha)
            print(item.committed_date)

            res = db_con_fileEdit.find(
                {'committed_date': item.committed_date, 'hexsha': item.hexsha}, limit=1, count=True)

            if not res:
                dic = {
                    'id': studentID,
                    'committed_date': item.committed_date,
                    'hexsha': item.hexsha
                }
                # print()
                # print(dic)
                db_con_fileEdit.insert(dic)


def main(argv):

    # 引数のリストにはファイルパスが指定させている
    file_path = argv[0]
    print(file_path)

    # DBを接続し、コレクションを作成
    db_con_fileEdit = DBController(db_name, db_col_fileEdit)

    '''
    引数から取得したfile_pathの値がDBにあるかどうかを確認
    1. DBでfile_pathをfindする
    if file_pathがDB上にない:
       2. このfile_pathをDB上に追加
       3. このfile_pathの_idを記録
       4. 以下の処理を行い_idのドキュメントにログ収集結果を追加
    '''

    # ファイルのパスを/で分割し、リスト化する
    file_path_list = file_path.split('/')
    # print(len(file_path_list))

    # gitリポジトリをgitbucketとDBに追加
    insert_fileEdit_data(db_con_fileEdit, file_path, file_path_list)


if __name__ == '__main__':
    main(sys.argv[1:])
