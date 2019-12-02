import sys
import glob
import pandas as pd
from mongo_connect import DBController

import tarfile

# DB名/コレクション名
db_name = "students"
db_col = "file_edit"


# script.tar.gzファイルを展開する
def open_tarfile(file_path):
    pass
    # scriptコマンドで収集したscript.tar.gzを展開
    # with tarfile.open(file_path, 'r:gz') as tf:
    # file_path[:-10]はgit.tar.gzまでのpathを意味している
    # tf.extractall(file_path[:-10])


def main(argv):
    db_con = DBController(db_name, db_col)
    # print(argv[0])
    file_path = argv[0]
    print(file_path)

    # 引数から取得したfile_pathの値がDBにあるかどうかを確認
    # 1. DBでfile_pathをfindする
    # if file_pathがDB上にない:
    #    2. このfile_pathをDB上に追加
    #    3. このfile_pathの_idを記録
    #    4. 以下の処理を行い_idのドキュメントにログ収集結果を追加

    file_path_list = file_path.split('/')
    print(len(file_path_list))

    if(len(file_path_list) == 8):
        # unixtimeを取得
        unixtime_str = file_path_list[6]
        unixtime = int(unixtime_str)
        print(unixtime)

        # ファイル名を取得
        file_name = file_path_list[7]
        print(file_name)
        # open_tarfile(file_path)
        #     db_con.insert(dic)


if __name__ == '__main__':
    main(sys.argv[1:])
