from fabric import Connection
from datetime import datetime
import socket
import sys
import re
import pandas as pd
pd.set_option("display.max_columns", 100)  # Number of columns in pandas output

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from env import settings


def run_server_cmd(id, df, host, group, con, cmd, step):
    result = con.run(cmd, warn=True)
    df_temp = pd.DataFrame([[datetime.now().strftime(
        '%s'), id, host, group, result.command, result.stdout.strip(), result.stderr.strip(), step]])
    df_temp.columns = ["unixtime", "id", "host",
                       "group", "command", "stdout", "stderr", "step"]
    return df.append(df_temp, sort=False)


def run_local_cmd(id, df, host, group, con, cmd, step):
    result = con.local(cmd, warn=True)
    df_temp = pd.DataFrame([[datetime.now().strftime(
        '%s'), id, host, group, result.command, result.stdout.strip(), result.stderr.strip(), step]])
    df_temp.columns = ["unixtime", "id", "host",
                       "group", "command", "stdout", "stderr", "step"]
    return df.append(df_temp, sort=False)


def check_server_status(key, st, host_addr, group):
    df = pd.DataFrame(index=[], columns=["unixtime", "id","host", "group", "command", "stdout", "stderr", "step"])
    command_id = st['command_id']
    run_type = st['run_type']
    command = st['command']

    # print(len(host_addr))
    for i, host in host_addr.iterrows():
        id = host['student_id']
        id = id + ((int)(group) * len(host_addr))
        h = host['ip_address']
        # print(key)
        # print(id)
        # print(h)

        try:
            print("--------------- students_id: " + (str)(id) + " ---------------")
            c = Connection(host=h, user="logger", port=22, connect_timeout=2, connect_kwargs={"key_filename": key})
            print("Connected host: "+h)

            backup_dir = settings.SYSTEM_LOG + group + "/status/" + command_id
            c.local("mkdir -p "+backup_dir, warn=True)
            print("Created backup_dir locally: "+backup_dir)

            #コマンド が一つでも失敗するとログの収集が行えない．
            if run_type == "run_server_cmd":
                df = run_server_cmd(id, df, h, group, c, command, command_id)
            elif run_type == "run_local_cmd":
                pattern = re.compile(r'ip_address')
                command = pattern.sub(h, command)
                df = run_local_cmd(id, df, h, group, c, command, command_id)
            print()
        except:
            print("{}: {}: {}".format(
                datetime.now().strftime('%s'), h, "socket.timeout"))
            df_temp = pd.DataFrame([[datetime.now().strftime(
                '%s'), id, h, "exception", "", "", "socket.timeout", "exception"]])
            df_temp.columns = ["unixtime", "team", "host",
                                "group", "command", "stdout", "stderr", "step"]
            df = df.append(df_temp, sort=False)
            continue
            df = df.append(df_temp)
    return df


if __name__ == '__main__':
    # arguments = sys.argv
    # if len(arguments)==1:
    #     sys.exit()
    # group = arguments[1]

    file_name = settings.SYSTEM_PATH + "/group_num"
    try:
        file = open(file_name)
        group = file.read()
        group = group.replace('\n', '')
        group = group.zfill(2)
        # print(group)
        # print(type(group))
    except Excepsion as e:
        print(e)
    # print(group)
    key = settings.SYSTEM_PATH + "/keys/id_rsa.pub"

    try:
        status = pd.read_csv(settings.SYSTEM_PATH + "/status_list.csv")
        host_df = pd.read_csv(settings.SYSTEM_PATH + "/ip_address.csv")

        print("--------------- Start collect log function ---------------")
        # sort option is added for avoiding FutureWarning
        for i, st in status.iterrows():
            df = pd.DataFrame(index=[],columns=["unixtime","id","host","group","command","stdout","stderr","step"]) #Empty dataframe
            command_id = st['command_id']
            command = st['command']
            print("--------------- server status command ---------------")
            print(command_id + ": " + command)
            print()
            df = df.append(check_server_status(key, st, host_df, group), ignore_index=True, sort=False)
            record_date = datetime.now().strftime('%s')
            df.to_csv(settings.SYSTEM_LOG + group + "/status/" + command_id + "/" + record_date + ".tsv", sep='\t', encoding='utf-8', quotechar='\'')
            # host_df.to_csv(record_date+".csv",sep=',', encoding='utf-8',quotechar='\'')

        print("--------------- Finish collect log function ---------------")
        print()

    except:
        print("No URL or File")
