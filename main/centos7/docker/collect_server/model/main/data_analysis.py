import sys
import glob
import pandas as pd
import numpy as np
from mongo_connect import DBController
import re
import html

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# DB名/コレクション名
db_name = "students"
collection = "status"
collection2 = "status_analysis"


def insert_status_data(status_col, file_path, file_path_list):

    # ファイルパスが特定の要素数あるファイルのみをDB追加処理にかける
    if(len(file_path_list) == 7):
        # リストの末尾の値はファイル名
        file_name = file_path_list[-1]

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
            '''
            引数から取得したfile_pathの値がDBにあるかどうかを確認
            1. DBでfile_pathをfindする
            if file_pathがDB上にない:
            2. このfile_pathをDB上に追加
            3. このfile_pathの_idを記録
            4. 以下の処理を行い_idのドキュメントにログ収集結果を追加
            '''

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
            status_col.insert(dic)


def insert_analysisStatus_data(status_analysis_col, file_path, file_path_list):

    # ファイルパスが特定の要素数あるファイルのみを分析処理にかける
    if (len(file_path_list) == 7):

        '''
        分析プログラムの処理手順
        0. 分析に必要なデータを変数に記録
        1. 最新のサーバ状況確認履歴の分析データを取得する (なければスキップ)
        2. 今回読み込まれたファイルのデータの値をクラスタリングする
            2-1. 標準出力のクラスタリング
            2-2. 標準エラー出力のクラスタリング
        3. 最新の分析データとクラスタリングデータを比較し、違いがあればupdateTimeを変更
        4. 多数決処理を行う
            4-1. クラスタリングされたグループ間のupdateTimeで平均値を取る
            4-2. 平均値が最も低いグループを排除
            4-3. 残りのグループの中から最も要素数の多いグループが正解であると推定する
        5. 読み込まれたクラスタリング結果をDBに入れる
        '''

        ##### 0. 分析に必要なデータを変数に記録 #####

        # ファイル名をfile_path_listから抽出
        file_name = file_path_list[-1]
        print('file_path: ', end="")
        print(file_path)

        # ステップ番号をfile_path_listから抽出
        step = file_path_list[5]
        print('step: ', end="")
        print(step)

        # ファイル名を分割してunixtimeを抽出
        file_name_list = file_name.split('.')
        # print(file_name_list)
        unixtime_str = file_name_list[0]
        # print(unixtime_str)
        unixtime = int(unixtime_str)
        print('unixtime: ', end="")
        print(unixtime)

        # csvファイル読み込み
        df = pd.read_csv(file_path, delimiter="\t",
                         quotechar='\'', index_col=0)

        # データ収集を行っている学生の人数
        student_num = len(list(df['id']))
        print('student_num: ', end="")
        print(student_num)

        # データが収集された詳しい時刻情報をupdate_timeリストとして保持
        stdout_time = list(df['unixtime'])
        stderr_time = list(df['unixtime'])

        ##### 1. 最新のサーバ状況確認履歴の分析データを取得する #####

        # DBから最新のデータを一つ取得する
        status_analysis = status_analysis_col.find(
            {'step': step}, 1, True, 'collection_time')

        status_analysis = list(status_analysis)
        print('status_analysis')
        print(status_analysis)

        status_analysis_len = len(status_analysis)
        print('status_analysis_len')
        print(status_analysis_len)

        if status_analysis_len == 0:
            status_analysis = {}
        else:
            status_analysis = status_analysis[0]

        # 最新のstdout_update_time
        if 'stdout_update_time' in status_analysis:
            stdout_update_time = status_analysis['stdout_update_time']
        else:
            stdout_update_time = [0 for i in range(student_num)]
        # 最新の標準出力のクラスタリング結果
        if 'stdout_clustering' in status_analysis:
            pre_stdout_clustering = status_analysis['stdout_clustering']
        else:
            pre_stdout_clustering = [0 for i in range(student_num)]
        print('pre_stdout_clustering: ', end="")
        print(pre_stdout_clustering)

        # 最新のstderr_update_time
        if 'stderr_update_time' in status_analysis:
            stderr_update_time = status_analysis['stderr_update_time']
        else:
            stderr_update_time = [0 for i in range(student_num)]

        # 最新の標準エラー出力のクラスタリング結果
        if 'stderr_clustering' in status_analysis:
            pre_stderr_clustering = status_analysis['stderr_clustering']
        else:
            pre_stderr_clustering = [0 for i in range(student_num)]
        print('pre_stderr_clustering: ', end="")
        print(pre_stderr_clustering)

        ##### 2. 今回読み込まれたファイルのデータの値をクラスタリングする #####

        # クラスタリング処理に必要のない要素の削除
        del(df['id'])
        del(df['unixtime'])
        del(df['host'])
        del(df['group'])
        del(df['command'])
        del(df['step'])
        # print(df['stdout'])

        ##### 2-1. 標準出力のクラスタリング #####

        # データを変換処理する(nanなどを文字列にする or 抽象化処理など..) *改善の余地あり
        stdout_list = list(
            map(lambda s: html.escape(str(s)), df['stdout']))
        stdout_list = [stdout for stdout in stdout_list if re.sub(
            r'[0-9]', "x", stdout)]

        print('stdout_list: ', end="")
        print(stdout_list)

        # stdout_list = ['aaa', 'aab', 'aaac', 'da']

        # 文字列をベクトル情報に変換処理
        stdout_vectorizer = TfidfVectorizer(stop_words='english')
        stdout_vector = stdout_vectorizer.fit_transform(stdout_list)
        # print('stdout_vector: ', end="")
        # print(stdout_vector)

        # クラスタリング処理
        stdout_true_k = 20
        stdout_model = KMeans(n_clusters=stdout_true_k, init='k-means++',
                              max_iter=100, n_init=1)
        stdout_model.fit(stdout_vector)

        # クラスタリング結果
        stdout_clustering = list(stdout_model.labels_)
        stdout_clustering = [int(stdout) for stdout in stdout_clustering]
        print('stdout_clustering')
        print(stdout_clustering)
        print('stdout_clustering type: ', end="")
        print(type(stdout_clustering))
        print()

        ##### 2-2. 標準エラー出力のクラスタリング #####

        # データを変換処理する(nanなどを文字列にする or 抽象化処理など..) *改善の余地あり
        stderr_list = list(
            map(lambda s: html.escape(str(s)), df['stderr']))
        stderr_list = [stderr for stderr in stderr_list if re.sub(
            r'[0-9]', "x", stderr)]
        print('stderr_list: ', end="")
        print(stderr_list)

        # stderr_list = ['aaa', 'aab', 'aaac', 'da']

        # 文字列をベクトル情報に変換処理
        stderr_vectorizer = TfidfVectorizer(stop_words='english')
        stderr_vector = stderr_vectorizer.fit_transform(stderr_list)
        # print('stderr_vector')
        # print(stderr_vector)

        # クラスタリング処理
        stderr_true_k = 20
        stderr_model = KMeans(n_clusters=stderr_true_k, init='k-means++',
                              max_iter=100, n_init=1)
        stderr_model.fit(stderr_vector)

        # クラスタリング結果
        stderr_clustering = list(stderr_model.labels_)
        stderr_clustering = [int(stderr) for stderr in stderr_clustering]
        print('stderr_clustering')
        print(stderr_clustering)
        print('stderr_clustering type: ', end="")
        print(type(stderr_clustering))
        print()

        ##### 3. 最新の分析データとクラスタリングデータを比較し、違いがあればupdateTimeを変更 #####

        # 標準出力のクラスタリング結果を比較
        stdout_update_time = [stdout_update_time[i] if pStdout == stdout else stdout_time[i]
                              for i, (pStdout, stdout) in enumerate(zip(pre_stdout_clustering, stdout_clustering))]
        print('stdout_update_time: ', end="")
        print(stdout_update_time)

        # 標準エラー出力のクラスタリング結果を比較
        stderr_update_time = [stderr_update_time[i] if pStderr == stderr else stderr_time[i]
                              for i, (pStderr, stderr) in enumerate(zip(pre_stderr_clustering, stderr_clustering))]
        print('stderr_update_time: ', end="")
        print(stderr_update_time)

        ##### 4. 多数決処理を行う #####

        # 4-1. クラスタリングされたグループ間のupdateTimeで平均値を取る

        # 標準出力のクラスタリング結果のset
        print(stdout_clustering)
        stdout_clustering_set = set(stdout_clustering)
        print('stdout_clustering_set: ', end="")
        print(stdout_clustering_set)

        # 標準出力のクラスタリング結果のupdate_timeの平均値
        stdout_clustering_update_time_average = []
        stdout_clustering_update_time_len_list = []
        for stdoutClusterNum in stdout_clustering_set:
            print('stdout_cluster_num: ', end="")
            print(stdoutClusterNum)
            # 同じ値でクラスタリングされたリストの平均値の抽出
            stdout_clustering_update_list = [updateTime for updateTime, cluster in zip(
                stdout_update_time, stdout_clustering) if cluster == stdoutClusterNum]
            print('stdout_clustering_update_list: ', end="")
            print(stdout_clustering_update_list)
            # 抽出されたリストの合計
            stdoutClusterUpdateSum = sum(stdout_clustering_update_list)
            print('stdoutClusterUpdateSum: ', end="")
            print(stdoutClusterUpdateSum)
            # 抽出されたリストの要素数
            stdoutClusterUpdateLen = len(stdout_clustering_update_list)
            print('stdoutClusterUpdateLen: ', end="")
            print(stdoutClusterUpdateLen)
            # 抽出されたリストの要素するをリスト化する
            stdout_clustering_update_time_len_list.append(
                stdoutClusterUpdateLen)
            # 抽出されたリストの平均値
            stdout_clustering_update_time_average.append(
                stdoutClusterUpdateSum/stdoutClusterUpdateLen)
        print('stdout_clustering_update_time_len_list: ', end="")
        print(stdout_clustering_update_time_len_list)
        print('stdout_clustering_update_time_average: ', end="")
        print(stdout_clustering_update_time_average)

        # 標準エラー出力のクラスタリング結果のset
        stderr_clustering_set = set(stderr_clustering)
        print('stderr_clustering_set: ', end="")
        print(stderr_clustering_set)

        # 標準エラー出力のクラスタリング結果のupdate_timeの平均値
        stderr_clustering_update_time_average = []
        stderr_clustering_update_time_len_list = []
        for stderrClusterNum in stderr_clustering_set:
            print('stderr_cluster: ', end="")
            print(stderrClusterNum)
            # 同じ値でクラスタリングされたリストの平均値の抽出
            stderr_clustering_update_list = [updateTime for updateTime, cluster in zip(
                stderr_update_time, stderr_clustering) if cluster == stderrClusterNum]
            print('stderr_clustering_update_list: ', end="")
            print(stderr_clustering_update_list)
            # 抽出されたリストの合計
            stderrClusterUpdateSum = sum(stderr_clustering_update_list)
            print('stderrClusterUpdateSum: ', end="")
            print(stderrClusterUpdateSum)
            # 抽出されたリストの要素数
            stderrClusterUpdateLen = len(stderr_clustering_update_list)
            print('stderrClusterUpdateLen: ', end="")
            print(stderrClusterUpdateLen)
            # 抽出されたリストの要素するをリスト化する
            stderr_clustering_update_time_len_list.append(
                stderrClusterUpdateLen)
            # 抽出されたリストの平均値
            stderr_clustering_update_time_average.append(
                stderrClusterUpdateSum / stderrClusterUpdateLen)
        print('stderr_clustering_update_time_len_list: ', end="")
        print(stderr_clustering_update_time_len_list)
        print('stderr_clustering_update_time_average: ', end="")
        print(stderr_clustering_update_time_average)

        # 4-2. 平均値が最も低いグループを課題が進んでいないグループとして記録

        # 標準出力の分析結果処理
        stdout_clustering_update_time_average_min_index = stdout_clustering_update_time_average.index(min(
            stdout_clustering_update_time_average))
        print('stdout_clustering_update_time_average_min_index: ', end="")
        print(stdout_clustering_update_time_average_min_index)

        stdout_clustering_update_time_average_max_index = stdout_clustering_update_time_average.index(max(
            stdout_clustering_update_time_average))
        print('stdout_clustering_update_time_average_max_index: ', end="")
        print(stdout_clustering_update_time_average_max_index)

        # 標準エラー出力の分析結果処理

        stderr_clustering_update_time_average_min_index = stderr_clustering_update_time_average.index(min(
            stderr_clustering_update_time_average))
        print('stderr_clustering_update_time_average_min_index: ', end="")
        print(stderr_clustering_update_time_average_min_index)

        stderr_clustering_update_time_average_max_index = stderr_clustering_update_time_average.index(max(
            stderr_clustering_update_time_average))
        print('stderr_clustering_update_time_average_max_index: ', end="")
        print(stderr_clustering_update_time_average_max_index)

        ##### 5. 読み込まれたクラスタリング結果をDBに入れる #####

        # データベースに挿入する値を辞書型で定義
        dic = {
            'step': step,
            'stdout_list': stdout_list,
            'stderr_list': stderr_list,
            'collection_time': unixtime,
            'stdout_update_time': stdout_update_time,
            'stdout_clustering': stdout_clustering,
            'stderr_update_time': stderr_update_time,
            'stderr_clustering': stderr_clustering,
            'stdout_average_min_index': stdout_clustering_update_time_average_min_index,
            'stdout_average_max_index': stdout_clustering_update_time_average_max_index,
            'stderr_average_min_index': stderr_clustering_update_time_average_min_index,
            'stderr_average_max_index': stderr_clustering_update_time_average_max_index
        }
        status_analysis_col.insert(dic)


def main(argv):

    # 引数のリストにはファイルパスが指定させている
    file_path = argv[0]

    # DBを接続し、コレクションを作成
    status_col = DBController(db_name, collection)
    status_analysis_col = DBController(db_name, collection2)

    # ファイルのパスを/で分割し、リスト化する
    file_path_list = file_path.split('/')
    # print(len(file_path_list))

    # サーバ状況確認履歴をDBに追加
    insert_status_data(collection, file_path, file_path_list)

    # 進捗状況を分析し、結果をDBに追加
    insert_analysisStatus_data(status_analysis_col, file_path, file_path_list)


if __name__ == '__main__':
    main(sys.argv[1:])
