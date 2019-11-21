if __name__ == "__main__":
    file_name = "/home/log_collect/group_num"
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
