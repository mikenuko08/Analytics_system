from fabric import Connection
from datetime import datetime
import socket
import sys
import re
import pandas as pd
pd.set_option("display.max_columns",100) #Number of columns in pandas output

# cat ~/user.dat
# def get_vmname(con):
#     try:
#         print(con)
#         result = con.run("cat ~/user.dat",warn = True)
#         if result.ok:
#             return result.stdout.strip()
#         else:
#             return result.stderr.strip()
#     except socket.timeout:
#         raise socket.timeout

def run_server_cmd(id, df, host, group, con, cmd, step):
    result = con.run(cmd, warn = True)
    df_temp = pd.DataFrame([[datetime.now().strftime('%s'),id,host,group,result.command,result.stdout.strip(),result.stderr.strip(),step]])
    df_temp.columns = ["unixtime","id","host","group","command","stdout","stderr","step"]
    return df.append(df_temp, sort=False)

def run_local_cmd(id, df, host, group, con, cmd, step):
    result = con.local(cmd, warn = True)
    df_temp = pd.DataFrame([[datetime.now().strftime('%s'),id,host,group,result.command,result.stdout.strip(),result.stderr.strip(),step]])
    df_temp.columns = ["unixtime","id","host","group","command","stdout","stderr","step"]
    return df.append(df_temp, sort=False)

    
def check_server_status(key, host_addr, group):
    df = pd.DataFrame(index=[],columns=["unixtime","id","host","group","command","stdout","stderr","step"])
    # print(len(host_addr))
    for i, row in host_addr.iterrows():
        id = row['student_id']
        id = id + ((int)(group) * len(host_addr))
        h = row['ip_address']
        print(key)
        print(id)
        print(h)
        
        try:
            print("--------------- Start check_server_status function "+(str)(id)+" ---------------")
            c = Connection(host=h,user="logger",port=22,connect_timeout=2,connect_kwargs={"key_filename":key})
            print("Connected host: "+h)

            backup_dir = "/home/log/" + group + "/status"
            c.local("mkdir -p "+backup_dir, warn=True)
            print("Created backup_dir locally: "+backup_dir)

            #コマンド が一つでも失敗するとログの収集が行えなくなってしまった．
            df = run_server_cmd(id, df, h, group, c, "yum list installed | grep httpd", "step1-1")
            print("step1-1")
            df = run_server_cmd(id, df, h, group, c,"systemctl status httpd", "step1-2")
            print("step1-2")
            df = run_server_cmd(id, df, h, group, c,"systemctl status firewalld", "step1-3")
            print("step1-3")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80 --connect-timeout 5 -sS", "step1-4")
            print("step1-4")
            df = run_server_cmd(id, df, h, group, c, "find /var/www/html/hello.txt", "step1-5-1")
            print("step1-5-1")
            df = run_server_cmd(id, df, h, group, c, "find /var/www/html/hellow.txt", "step1-5-2")
            print("step1-5-2")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80/hello.txt --connect-timeout 5 -sS", "step1-6-1")
            print("step1-6-1")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80/hellow.txt --connect-timeout 5 -sS", "step1-6-2")
            print("step1-6-2")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80 --connect-timeout 5 -sS", "step1-7")
            print("step1-7")
            df = run_server_cmd(id, df, h, group, c, "tail -n 3 /var/log/httpd/access_log", "step2")
            print("step2")
            df = run_server_cmd(id, df, h, group, c,"find /var/www/html/ensyu.txt", "step3-1")
            print("step3-1")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80/ensyu.txt --connect-timeout 5 -sS", "step3-2")
            print("step3-2")
            #df = run_server_cmd(id,df,h,group,c,"find /var/www/rootdirectory","step4-1")
            #print("step4-1")
            df = run_server_cmd(id, df, h, group, c, "find /var/www/rootdirectory/ensyu.txt", "step4-2")
            print("step4-2")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":80/ensyu.txt --connect-timeout 5 -sS", "step4-3")
            print("step4-3")
            df = run_server_cmd(id, df, h, group, c, "cat /etc/httpd/conf/httpd.conf | grep Listen", "step5-1")
            print("step5-1")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":443 --connect-timeout 5 -sS", "step5-2")
            print("step5-2")
            df = run_server_cmd(id, df, h, group, c, "cat /etc/httpd/conf/httpd.conf | grep DirectoryIndex", "step6-1")
            print("step6-1")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":443 --connect-timeout 5 -sS", "step6-2")
            print("step6-2")
            df = run_server_cmd(id, df, h, group, c,  "systemctl status firewalld", "step7-1")
            print("step7-1")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h + ":443 --connect-timeout 5 -sS", "step7-2")
            print("step7-2")
            df = run_server_cmd(id, df, h, group, c,  "yum list installed | grep php", "step8-1")
            print("step8-1")
            df = run_server_cmd(id, df, h, group, c,  "systemctl status httpd", "step8-2")
            print("step8-2")
            df = run_server_cmd(id, df, h, group, c, "find /var/www/rootdirectory/ensyu.txt", "step8-3")
            print("step8-3")
            df = run_local_cmd(id, df, h, group, c, "curl http://" + h+":443/phptest.php --connect-timeout 5 -sS", "step8-4")
            print("step8-4")

            print("--------------- Finish check_server_status function ---------------")
            print()
        except:
            print("{}: {}: {}".format(datetime.now().strftime('%s'),h,"socket.timeout"))
            df_temp = pd.DataFrame([[datetime.now().strftime('%s'),id,h,"exception","","","socket.timeout","exception"]])
            df_temp.columns = ["unixtime","team","host","group","command","stdout","stderr","step"]
            df = df.append(df_temp, sort=False)
            continue
            df = df.append(df_temp)
    return df


if __name__ == '__main__':
    # arguments = sys.argv
    # if len(arguments)==1:
    #     sys.exit()
    # group = arguments[1]

    file_name = "/home/log_collect/group_num"
    try:
        file = open(file_name)
        group = file.read()
        group = group.replace('\n','')
        group = group.zfill(2)
        # print(group)
        # print(type(group))
    except Excepsion as e:
        print(e)
    # print(group)
    key = "/home/log_collect/id_rsa.pub"
    
    try:
        host_df = pd.read_csv("/home/log_collect/ip_address.csv")
        df = pd.DataFrame(index=[],columns=["unixtime","id","host","group","command","stdout","stderr","step"]) #Empty dataframe
        #sort option is added for avoiding FutureWarning
        df = df.append(check_server_status(key, host_df, group), ignore_index=True, sort=False)
        record_date = datetime.now().strftime('%s')
        df.to_csv("/home/log/"+group+"/status/"+record_date+".tsv",sep='\t', encoding='utf-8',quotechar='\'')
        #host_df.to_csv(record_date+".csv",sep=',', encoding='utf-8',quotechar='\'')
    except:
        print("No URL or File")
