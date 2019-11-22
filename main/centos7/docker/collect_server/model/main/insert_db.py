import sys
import glob
import pandas as pd
from mongo_connect import DBController
pd.set_option("display.max_columns", 100)  # Number of columns in pandas output
pd.set_option("display.max_colwidth", 200)
pd.set_option("display.max_rows", 100)

log_file = "read_file.log"


def main(argv):
    # 記録を行うデータベースをインスタンス化
    controller = DBController()
    # 接続するコレクション変数
    collection = "status"

    # 指定されたディレクトリ以下の全ファイルパスを取得
    file_paths = sorted(glob.glob("/root/log/00/status/*.tsv"))

    size = 0
    for file_path in file_paths:
        # 挿入済みのtsvファイルを記録しているファイルを開く
        with open(log_file, "r") as f:
            flag = False
            line = f.readline()
            while line:
                # DBに追記済みのファイルかどうか
                if file_path in line:
                    flag = True
                line = f.readline()

            ''' 
			もしDBに追記されていないファイルであれば,
			ログファイルに記録し、データをDBに挿入
			'''
            if not flag:
                with open(log_file, "a") as f:
                    f.write("{}\n".format(file_path))

                print(file_path)
                file_path_list = file_path.split('/')
                # ファイル名取得
                file_name = file_path_list[5]

                # ファイル名を分割してunixtimeを抽出
                file_name_list = file_name.split('.')
                unixtime_str = file_name_list[0]
                unixtime = int(unixtime_str)

                # 秒数を端折る
                de = unixtime % 60
                unixtime = int(unixtime - de)
                # print(unixtime)
                # pandasに読み込む
                df = pd.read_csv(file_path, delimiter="\t",
                                 quotechar='\'', index_col=0)

                for row in df.itertuples():
                    # データベースに挿入する値を辞書型で定義
                    d = {
                        'id': int(row.id),
                        'host': row.host,
                        'group': int(row.group),
                        'command': row.command,
                        'stdout': row.stdout,
                        'stderr': row.stderr,
                        'step': row.step,
                        'date': int(row.unixtime),
                        'unixtime': int(unixtime),
                    }
                    # データベースに挿入処理
                    size = size + 1
                    # print(size)
                    if size == 83:
                        print(file_path)
                    st_db.insert(collection, d)


if __name__ == '__main__':
    main(sys.argv[1:])
