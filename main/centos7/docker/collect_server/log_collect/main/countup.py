# coding: UTF-8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from env import settings

if __name__ == "__main__":
    file_name = settings.SYSTEM_PATH + "/group_num"
    try:
        file1 = open(file_name)
        group = file1.read()
        file1.close()
        num = (int)(group) + 1
        print(num)
        # print(type(num))
    except Exception as e:
        print(e)

    try:
        file2 = open(file_name, "w")
        file2.write((str)(num))
        file2.close()
    except Exception as e:
        print(e)
