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


def analysis_init(file_path):
    file_path_list = file_path.split('/')
    # ファイルパスが特定の要素数あるファイルのみを分析処理にかける
    if (len(file_path_list) == 6):
        # ファイル名をfile_path_listから抽出
        file_name = file_path_list[-1]
        # ファイル名を分割してcollection_timeを抽出
        file_name_list = file_name.split('.')
        # print(file_name_list)
        collection_time_str = file_name_list[0]
        # print(unixtime_str)
        collection_time = int(collection_time_str)
        print('collection_time: ', end="")
        print(collection_time)
        return collection_time
    else:
        sys.exit()


def insert_status_data(status_col, file_path):

    # collection_timeを保持
    collection_time = analysis_init(file_path)
    print(collection_time)
    print(type(collection_time))
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
            'collection_time': collection_time,
        }
        status_col.insert(dic)


# 必要なデータをDBから検索しリストを返す
def get_database_list(status_col, step, time, feild=''):
    # 引数で指定したstepとtimeに一致したDBの値を取得
    status_list = list(status_col.find(
        {'step': step, 'collection_time': time}))
    # print('status_list')
    # print(status_list)

    # 特定のフィールドの値のみを抽出
    result = list(status[feild] for status in status_list)
    print(result)

    return result


# データを変換処理する(nanなどを文字列にする or 抽象化処理など..) *改善の余地あり
def data_transform(data_list):
    format_list = list(
        map(lambda s: html.escape(str(s)), data_list))
    result_list = [result for result in format_list if re.sub(
        r'[0-9]', "x", result)]

    # print('result_list: ', end="")
    # print(result_list)
    return result_list

 # 文字列をベクトル情報に変換処理


def data_transform_to_vector(data_list):
    vectorizer = TfidfVectorizer(stop_words='english')
    data_vector = vectorizer.fit_transform(data_list)
    # print('vector: ', end="")
    # print(vector)
    return data_vector


# クラスタリング処理
def data_clustering(student_num, data_vector):
    true_k = student_num
    model = KMeans(n_clusters=true_k, init='k-means++',
                   max_iter=100, n_init=1)
    model.fit(data_vector)

    # クラスタリング結果
    clustering = list(model.labels_)
    clustering = [int(value) for value in clustering]
    # print('clustering')
    # print(clustering)
    # print('clustering type: ', end="")
    # print(type(clustering))
    # print()

    return clustering


# データ分析処理
def data_analysis(student_num, data_list):
    data = data_transform(data_list)
    data_vector = data_transform_to_vector(data)
    clustering = data_clustering(student_num, data_vector)
    return clustering


# クラスタリング結果のdiffを取り結果が異なれば、updatetimeを更新する
def clustering_result_diff(update_time, pre_collection_time, leatest_collection_time, pre_clustering, leatest_clustering):
    print(update_time)
    print(pre_collection_time)
    print(leatest_collection_time)
    print(pre_clustering)
    print(leatest_clustering)

    if len(update_time) == 0:
        update_time = pre_collection_time

    for i, (result1, result2) in enumerate(zip(pre_clustering, leatest_clustering)):
        print(update_time[i])
        print(leatest_collection_time[i])
        if result1 != result2:
            update_time[i] = leatest_collection_time[i]
        else:
            update_time[i] = update_time[i]

    return update_time


def update_time_average_list(clustering_result, update_time):
    # 標準出力のクラスタリング結果のset
    clustering_set = set(clustering_result)
    print('clustering_set: ', end="")
    print(clustering_set)

    # 標準出力のクラスタリング結果のupdate_timeの平均値
    clustering_update_time_average_list = []

    for clusterNum in clustering_set:
        print('cluster_num: ', end="")
        print(clusterNum)
        # 同じ値でクラスタリングされたリストの平均値の抽出
        clustering_update_list = [updateTime for updateTime, cluster in zip(
            update_time, clustering_result) if cluster == clusterNum]
        print('clustering_update_list: ', end="")
        print(clustering_update_list)
        # 抽出されたリストの合計
        clusterUpdateSum = sum(clustering_update_list)
        print('clusterUpdateSum: ', end="")
        print(clusterUpdateSum)
        # 抽出されたリストの要素数
        clusterUpdateLen = len(clustering_update_list)
        print('clusterUpdateLen: ', end="")
        print(clusterUpdateLen)
        # 抽出されたリストの平均値
        clustering_update_time_average_list.append(
            clusterUpdateSum/clusterUpdateLen)
    print('clustering_update_time_average_list: ', end="")
    print(clustering_update_time_average_list)

    return clustering_update_time_average_list


def insert_analysisStatus_data(status_col, status_analysis_col, analysis_field, file_path):

    # collection_timeを保持
    collection_time = analysis_init(file_path)

    ##### 1. 最新のサーバ状況確認履歴の分析データを取得する #####

    # DBからデータを収集した時刻を取得する
    collection_time_list = list(status_col.distinct('collection_time'))
    print('collection_time_list: ', end="")
    print(collection_time_list)

    # 収集した時刻の数
    collection_time_len = len(collection_time_list)
    print('collection_time_len: ', end="")
    print(collection_time_len)

    # サーバ状況確認コマンドのリストを取得
    step_list = list(status_col.distinct('step'))
    print(step_list)

    # 学生のリストを取得
    student_list = list(status_col.distinct('id'))
    student_num = len(student_list)
    print(student_num)

    # 最新の時刻情報
    leatest_time = collection_time_list[-1]
    print('leatest_time: ', end="")
    print(leatest_time)
    # 収集した最新時刻
    leatest_detail_collection_time = []
    # analysis_fieldのリスト
    leatest_list = []
    pre_detail_collection_time = []
    pre_list = []
    update_time = [0 for i in range(student_num)]
    min_index = -1
    max_index = -1

    # 収集したデータが2つ以上の時データを分析処理をする
    if collection_time_len >= 2:
        # 最新の一つ前の時刻情報
        pre_time = collection_time_list[-2]
        print('pre_time: ', end="")
        print(pre_time)

    for step in step_list:
        print('###### step: ' + step + ' ######')

        # 時刻情報の処理
        # 最新収集時刻のリスト
        print('leatest_collection_time')
        leatest_collection_time = get_database_list(
            status_col, step, leatest_time, feild='detail_collection_time')

        # 収集したデータが2つ以上の時データを分析処理をする
        if collection_time_len >= 2:
            # 最新時刻よりひとつ前の収集時刻のリスト
            print('pre_collection_time')
            pre_collection_time = get_database_list(
                status_col, step, pre_time, feild='detail_collection_time')

        ##### 2. 今回読み込まれたファイルのデータの値をクラスタリングする #####

        ##### 2-1. analysis_fieldのリストデータのクラスタリング処理 #####
        # 最新のanalysis_fieldのリスト
        print('leatest_list')
        leatest = get_database_list(
            status_col, step, leatest_time, feild=analysis_field)
        # 最新のanalysis_fieldのリストのクラスタリング
        leatest_clustering = data_analysis(
            student_num, leatest)
        print(leatest_clustering)

        # 収集したデータが2つ以上の時データを分析処理をする
        if collection_time_len >= 2:
            # 最新よりひとつ前の時刻のanalysis_fieldのリスト取得
            print('pre_list')
            pre = get_database_list(
                status_col, step, pre_time, feild=analysis_field)
            # 最新よりひとつ前のanalysis_fieldのリストのクラスタリング
            pre_clustering = data_analysis(student_num, pre)
            print(pre_clustering)

            ##### 3. 最新の分析データとクラスタリングデータを比較し、違いがあればupdateTimeを変更 #####
            update_time = get_database_list(
                status_analysis_col, step, pre_time, feild='update_time')
            update_time = update_time[0]
            print("update_time")
            print(update_time)
            print()

            update_time_diff = clustering_result_diff(
                update_time, pre_collection_time, leatest_collection_time, pre_clustering, leatest_clustering)

            print("update_time_diff")
            print(update_time_diff)
            print()

            ##### 4. 多数決処理を行う #####

            # 4-1. クラスタリングされたグループ間のupdateTimeで平均値を取る

            # 標準出力のupdate_timeの平均値のリスト
            update_time_average = update_time_average_list(
                leatest_clustering, update_time_diff)

            # 4-2. 平均値が最も低いグループを課題が進んでいないグループとして記録

            # 標準出力の分析結果処理
            min_index = update_time_average.index(
                min(update_time_average))
            print('clustering_update_time_average_min_index: ', end="")
            print(min_index)

            max_index = update_time_average.index(max(
                update_time_average))
            print('clustering_update_time_average_max_index: ', end="")
            print(max_index)

        ##### 5. 読み込まれたクラスタリング結果をDBに入れる #####

        # データベースに挿入する値を辞書型で定義
        dic = {
            'analysis_field': analysis_field,
            'step': step,
            'collection_time': collection_time,
            'update_time': update_time,
            'average_min_index': min_index,
            'average_max_index': max_index,
        }
        status_analysis_col.insert(dic)


def main(argv):

    # 引数のリストにはファイルパスが指定させている
    file_path = argv[0]
    print(file_path)

    # DBを接続し、コレクションを作成
    status_col = DBController(db_name, collection)
    status_analysis_col = DBController(db_name, collection2)

    # サーバ状況確認履歴をDBに追加
    insert_status_data(status_col, file_path)

    # 進捗状況を分析し、結果をDBに追加
    analysis_field1 = 'stdout'
    analysis_field2 = 'stderr'

    insert_analysisStatus_data(
        status_col, status_analysis_col, analysis_field1, file_path)
    # insert_analysisStatus_data(
    #     status_col, status_analysis_col, analysis_field2, file_path)


if __name__ == '__main__':
    main(sys.argv[1:])
