import sys
import glob
import pandas as pd
from mongo_connect import DBController

import html

# DB名/コレクション名
db_name = "students"
db_col = "status"


def main(argv):
    db_con = DBController(db_name, db_col)
    # print(argv[0])
    file_path = argv[0]

    # 引数から取得したfile_pathの値がDBにあるかどうかを確認
    # 1. DBでfile_pathをfindする
    # if file_pathがDB上にない:
    #    2. このfile_pathをDB上に追加
    #    3. このfile_pathの_idを記録
    #    4. 以下の処理を行い_idのドキュメントにログ収集結果を追加

    file_path_list = file_path.split('/')
    # print(len(file_path_list))

    if(len(file_path_list) == 7):
        # ファイル名取得
        file_name = file_path_list[6]

        # ファイル名を分割してunixtimeを抽出
        file_name_list = file_name.split('.')
        unixtime_str = file_name_list[0]
        print(file_name_list)
        unixtime = int(unixtime_str)

        # print(unixtime)
        # pandasに読み込む
        df = pd.read_csv(file_path, delimiter="\t",
                         quotechar='\'', index_col=0)

        # print(df.fillna("NaN"))
        for row in df.itertuples():
            # データベースに挿入する値を辞書型で定義
            dic = {
                'file_path': file_path,
                'id': int(row.id),
                'host': row.host,
                'group': int(row.group),
                'command': row.command,
                'stdout': html.escape(str(row.stdout)),
                'stderr': html.escape(str(row.stderr)),
                'step': row.step,
                'detail_collection_time': int(row.unixtime),
                'collection_time': int(unixtime),
            }
            db_con.insert(dic)


if __name__ == '__main__':
    main(sys.argv[1:])
