import sys
import glob
import pandas as pd
from mongo_connect import DBController

import tarfile
from unicodedata import category
import curses.ascii as ca

import html

# DB名/コレクション名
db_name = "students"
db_col_history = "command_history"
db_col_script = "command_script"


# ファイルの内容をリストとして返却する
def history_file_read(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return lines


# 特殊文字を削除して、ファイルの内容をリストとして返却する
def script_file_read(file_path):
    # テキストファイルから文字列を読み込む
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read()

    # 読み込んだ文字列のCR(\r)を削除する。
    lines = lines.replace('\r', '')

    # print(lines)

    # ファイルをバイナリモードで開く
    with open(file_path, 'wb') as f:
        # 文字列をバイト列にして保存する
        f.write(lines.encode('utf-8'))

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return lines


# script.tar.gzファイルを展開する
def open_tarfile(file_path):
        # scriptコマンドで収集したscript.tar.gzを展開
    with tarfile.open(file_path, 'r:gz') as tf:
            # file_path[:-13]はscript.tar.gzまでのpathを意味している
        tf.extractall(file_path[:-13])


# .command_historyのデータをDBに追加
def insert_history_data(db_con_history, file_path, file_path_split_list):

    # group番号を取得
    group = int(file_path_split_list[3])
    # 学生番号 idを取得
    id = file_path_split_list[5]
    # collect_timeを取得
    collect_time = int(file_path_split_list[6])
    # print(collect_time)

    # ファイル名を取得
    file_name = file_path_split_list[7]
    # print(file_name)

    # .command_historyファイルを読み込み
    lines = history_file_read(file_path)
    for i, line in enumerate(lines):
        # print(i, line)

        if i % 3 == 0:
            # print('time_before_execution: ' + line[1:])
            time_before_execution = int(line[1:])
        elif i % 3 == 1:
            # print('command: ' + line)
            command = line
        elif i % 3 == 2:
            result = line.split('\t')
            for j, l in enumerate(result):
                l = l.split(':')
                if j % 3 == 0:
                    # print('status_code: ' + l[-1])
                    status_code = l[-1]
                elif j % 3 == 1:
                    # print('pwd: ' + l[-1])
                    pwd = l[-1]
                elif j % 3 == 2:
                    # print('time_afer_execution: ' + l[-1])
                    time_after_execution = int(l[-1])

                    '''
                    引数から取得したfile_pathの値がDBにあるかどうかを確認
                    1. DBでfile_pathをfindする
                    if file_pathがDB上にない:
                    2. このfile_pathをDB上に追加
                    3. このfile_pathの_idを記録
                    4. 以下の処理を行い_idのドキュメントにログ収集結果を追加
                    '''

                    row_num = i

                    collection_time_list = list(
                        db_con_history.distinct('collection_time'))
                    print(collection_time_list)
                    collect_time_flag = collect_time not in collection_time_list
                    print(collect_time_flag)

                    time_before_execution_list = list(
                        db_con_history.distinct('time_before_execution'))
                    print(time_before_execution_list)
                    time_before_execution_flag = time_before_execution not in time_before_execution_list
                    print(time_before_execution_flag)

                    time_after_execution_list = list(
                        db_con_history.distinct('time_after_execution'))
                    print(time_after_execution_list)
                    time_after_execution_flag = time_after_execution not in time_after_execution_list
                    print(time_after_execution_flag)

                    if collect_time_flag and time_before_execution_flag or time_after_execution_flag:

                        # データベースに挿入する値を辞書型で定義
                        dic = {
                            'row_num': row_num,
                            'file_path': file_path,
                            'group': group,
                            'id': id,
                            'collect_time': collect_time,
                            'time_before_execution': time_before_execution,
                            'time_after_execution': time_after_execution,
                            'pwd': pwd,
                            'command': command,
                            'status_code': status_code
                        }
                        # print()
                        # print(dic)
                        db_con_history.insert(dic)


def containsControlCharacter(s):
    return any(map(lambda c: category(c) == 'Cc', s))


# scriptのデータをDBに追加
def insert_script_data(db_con_script, file_path, file_path_list):
    # group番号を取得
    group = int(file_path_list[3])
    # 学生番号 idを取得
    id = file_path_list[5]
    # unixtimeを取得
    unixtime = int(file_path_list[6])
    # print(unixtime)

    # ファイル名を取得
    file_name = file_path_list[8]
    # print(file_name)

    # (unixtime)_root.logファイルを読み込み
    lines = script_file_read(file_path)
    executed_time = 0
    result = []
    for i, line in enumerate(lines):

        line_split = line.split(' ')

        # 次の行の0番目の値が時刻情報かどうか判定
        if line_split[0].isdecimal():
            # インサート処理
            if i != 0:
                print(executed_time)
                print(result)
                print(line)

                '''
                引数から取得したfile_pathの値がDBにあるかどうかを確認
                1. DBでfile_pathをfindする
                if file_pathがDB上にない:
                2. このfile_pathをDB上に追加
                3. このfile_pathの_idを記録
                4. 以下の処理を行い_idのドキュメントにログ収集結果を追加
                '''

                res = db_con_script.find(
                    {'row_num': i, 'file_name': file_name}, limit=1, count=True)
                if not res:
                    dic = {
                        'row_num': i,
                        'file_name': file_name,
                        'file_path': file_path,
                        'group': group,
                        'id': id,
                        'collect_time': unixtime,
                        'executed_time': executed_time,
                        'result': html.escape(str(result))
                    }
                    print(dic)
                    db_con_script.insert(dic)
                    result = []

            # 新しいコマンド実行時刻を保持
            executed_time = int(line_split[0])
            # 新しいコマンドの実行結果を保持
            result.append(' '.join(line_split[1:]))
        else:
            # 時刻情報でない時resultにline(時刻を含まない実行)を追加する
            result.append(line)
            continue


def main(argv):

    # 引数のリストにはファイルパスが指定させている
    file_path = argv[0]
    print(file_path)

    # DBを接続し、コレクションを作成
    db_con_history = DBController(db_name, db_col_history)
    db_con_script = DBController(db_name, db_col_script)

    # ファイルのパスを/で分割し、リスト化する
    file_path_list = file_path.split('/')
    # print(len(file_path_list))

    # リストの末尾の値はファイル名
    file_name = file_path_list[-1]

    # file_pathの末尾の文字列毎に処理を変える
    # 末尾が.tar.gzの場合
    if 'script.tar.gz' in file_name:
        # tar.gzファイルを解凍する処理
        print(file_name)
        open_tarfile(file_path)
    # 末尾が.command_hitoryの場合
    elif '.command_history' in file_name:
        # command_historyのログファイルの内容をDBに追加
        print(file_name)
        insert_history_data(db_con_history, file_path, file_path_list)
    # 末尾が_root.logの場合
    elif '_root.log' in file_name:
        # scriptコマンドのログファイルの内容をDBに追加
        print(file_name)
        insert_script_data(db_con_script, file_path, file_path_list)


if __name__ == '__main__':
    main(sys.argv[1:])
