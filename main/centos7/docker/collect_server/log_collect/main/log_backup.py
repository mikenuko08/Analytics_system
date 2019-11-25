from fabric import Connection
from datetime import datetime
import socket
import sys
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from env import settings


def get_vmname(con):
    try:
        print(con)
        result = con.run("cat ~/user.dat", warn=True)
        if result.ok:
            return result.stdout.strip()
        else:
            return "no-name"
    except socket.timeout:
        raise socket.timeout

# /git (ファイル編集履歴のログ)


def get_git_logs(key, host_addr, group):
    str_date = datetime.now().strftime('%s')
    for i, row in enumerate(host_addr):
        id = row['student_id']
        id = id + ((int)(group)*24)
        id = (str)(id)

        h = row['ip_address']
        # print(id)
        # print(type(id))
        # print(h)
        # print(group)

        try:
            print("Start get_git_logs function")
            c = Connection(host=h, user="root", port=22,
                           connect_timeout=2, connect_kwargs={"key_filename": key})
            print("Success connection host: "+h)

            #vmname = get_vmname(c)
            #print("Success get_vmname function: "+vmname)

            backup_dir = settings.SYSTEM_LOG + group + \
                "/command/" + id.zfill(3) + "/" + str_date
            c.local("mkdir -p "+backup_dir, warn=True)
            print("Create backup_dir locally: "+backup_dir)

            # c.run("mkdir -p "+backup_dir, warn=True)
            # print("Create backup_dir on remote: "+backup_dir)

            c.run("tar czf /root/git.tar.gz"+" -C / git", warn=True)
            print("Create git.tar.gz on remote")

            c.get("/root/git.tar.gz", backup_dir+"/git.tar.gz")
            print("Get git.tar.gz on remote")

            c.run("rm -rf /root/git.tar.gz", warn=True)
            print("Delete git.tar.gz on remote")

            print("Finish get_git_logs function")
        except socket.timeout:
            continue

# /var/log/script /root/.bash_history (コマンド実行履歴のログ)


def get_logs(key, host_addr, group):
    str_date = datetime.now().strftime('%s')
    # print(len(host_addr))
    for i, row in enumerate(host_addr):
        id = row['student_id']
        id = id + ((int)(group)*len(host_addr))
        id = (str)(id)
        h = row['ip_address']
        # print(id)
        # print(type(id))
        # print(h)
        # print(group)

        try:
            print("Start get_logs function")
            c = Connection(host=h, user="root", port=22,
                           connect_timeout=2, connect_kwargs={"key_filename": key})
            print("Success connection host: "+h)

            #vmname = get_vmname(c)
            #print("Success get_vmname function: "+vmname)

            backup_dir = settings.SYSTEM_LOG + group + \
                "/command/" + id.zfill(3) + " /" + str_date
            c.local("mkdir -p "+backup_dir, warn=True)
            print("Create backup_dir locally: "+backup_dir)

            # c.run("mkdir -p "+backup_dir, warn=True)
            # print("Create backup_dir on remote: "+backup_dir)

            c.run("tar czf /root/script.tar.gz -C /var/log/ script", warn=True)
            print("Create script.tar.gz on remote")

            c.get("/root/script.tar.gz", backup_dir+"/script.tar.gz")
            print("Get script.tar.gz on remote")

            c.run("rm -rf /root/script.tar.gz", warn=True)
            print("Delete script.tar.gz on remote")

            c.get("/root/.command_history", backup_dir+"/.command_history")
            print("Get .command_history on remote")

            print("Finish get_logs function")
        except socket.timeout:
            continue

# /var/log/script /root/.bash_history (コマンド実行履歴のログ) かつ /git (ファイル編集履歴のログ)


def get_all_logs(key, host_addr, group):
    str_date = datetime.now().strftime('%s')
    for i, row in host_addr.iterrows():
        id = row['student_id']
        id = id + ((int)(group)*len(host_addr))
        id = (str)(id)
        h = row['ip_address']
        # print(id)
        # print(type(id))
        # print(h)
        # print(group)

        try:
            print("--------------- Start get_all_logs function " +
                  id.zfill(3)+" ---------------")
            c = Connection(host=h, user="logger", port=22,
                           connect_timeout=5, connect_kwargs={"key_filename": key})
            print("Connected host: "+h)

            #vmname = get_vmname(c)
            #print("Executed get_vmname function: "+vmname)

            logger_dir = "/home/logger/log"
            command_backup_dir = settings.SYSTEM_LOG + group + \
                "/command/" + id.zfill(3) + "/" + str_date
            c.local("mkdir -p " + command_backup_dir, warn=True)
            print("Created command_backup_dir locally: " + command_backup_dir)

            c.run("sudo mkdir -p " + logger_dir, warn=True)
            print("Create command_backup_dir on remote: "+logger_dir)

            c.run("sudo tar czf " + logger_dir +
                  "/script.tar.gz -C /var/log/ script", warn=True)
            print("Created script.tar.gz on remote")

            c.get("/home/logger/log/script.tar.gz",
                  command_backup_dir + "/script.tar.gz")
            print("Get script.tar.gz on remote")

            c.run("sudo rm -rf " + logger_dir + "/script.tar.gz", warn=True)
            print("Deleted script.tar.gz on remote")

            c.run("sudo cp /root/.command_history " + logger_dir, warn=True)
            print(
                "Copy /root/.command_history to " + logger_dir + "/.command_history on remote")

            c.get(logger_dir + "/.command_history",
                  command_backup_dir + "/.command_history")
            print("Get .command_history on remote")

            file_edit_backup_dir = settings.SYSTEM_LOG + group + \
                "/file_edit/" + id.zfill(3) + "/" + str_date
            c.local("mkdir -p " + file_edit_backup_dir, warn=True)
            print("Created file_edit_backup_dir locally: " + file_edit_backup_dir)
            c.run("sudo tar czf " + logger_dir +
                  "/git.tar.gz -C / git", warn=True)
            print("Created git.tar.gz on remote")

            c.get(logger_dir + "/git.tar.gz",
                  file_edit_backup_dir + "/git.tar.gz")
            print("Get git.tar.gz on remote")

            c.run("sudo rm -rf " + logger_dir + "/git.tar.gz", warn=True)
            print("Deleted git.tar.gz on remote")

            print("--------------- Finish get_all_logs function ---------------")
            print()
        except socket.timeout:
            continue


# /var/log/script /root/.bash_history /git
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

    # arguments.pop(0)
    #options = [option for option in arguments if option.startswith('-')]

    try:
        host_df = pd.read_csv(settings.SYSTEM_PATH + "/ip_address.csv")
        get_all_logs(key, host_df, group)
        # if '-full' in options:
        #     get_git_logs(key,host_df.values.tolist()[0], group)
    except:
        print("No URL or File")
