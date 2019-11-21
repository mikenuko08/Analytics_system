import glob
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 指定されたディレクトリ以下の全ファイルパスを取得
file_paths = sorted(glob.glob("/root/log/00/status/*.tsv"))
# 読込むファイルのパスを宣言する

for file_path in file_paths:
    # print(file_paths)
    file_path_list = file_path.split('/')
    # ファイル名取得
    file_name = file_path_list[5]

    # ファイル名を分割してunixtimeを抽出
    file_name_list = file_name.split('.')
    unixtime_str = file_name_list[0]
    unixtime = int(unixtime_str)
    print("pretime")
    print(unixtime)

    # 秒数を端折る
    de = unixtime % 60
    unixtime = int(unixtime - de)
    print("nowtime")
    print(unixtime)
