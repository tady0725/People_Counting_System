import mysql.connector
from mysql.connector import Error
import datetime
s = datetime.datetime.now()
# dt = str(s).split(' ')
# d = str(dt[1]).split('.')

# time_now = str(dt[0]) + str(d[0])

# print(datetime.datetime.now())
# print(time_now)

def conection_DB():

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='ai_center', # 資料庫名稱
            user='root',        # 帳號
            password='')  # 密碼

        if connection.is_connected():

            # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("目前使用的資料庫：", record)

            # sql = "INSERT INTO `flow_people` (`ID`, `in_`, `out_`, `time_`) VALUES (NULL, %s, %s, %s);"
            # new_data = ('55', '60', str(s))
            # print(new_data)
            # cursors = connection.cursor()
            # cursors.execute(sql, new_data)


            

    except Error as e:
        print("資料庫連接失敗：", e)
    return connection

def insert_5min(ins,outs,times,connection):
    # 新增資料
    sql = "INSERT INTO `flow_people` (`ID`, `in_`, `out_`, `time_`) VALUES (NULL , %s, %s, %s);"
    new_data = (str(ins), str(outs), times)
    print(new_data)

    cursor = connection.cursor()
    cursor.execute(sql, new_data)
    # 確認資料有存入資料庫
    connection.commit()
def insert_hour(ins,outs,times,connection):
    # 新增資料
    sql = "INSERT INTO `hour_count` (`id`, `in_`, `out_`, `time_`) VALUES (NULL , %s, %s, %s);"
    new_data = (str(ins), str(outs), times)
    print(new_data)

    cursor = connection.cursor()
    cursor.execute(sql, new_data)
    # 確認資料有存入資料庫
    connection.commit()


    
    # sql = "INSERT INTO `flow_people` (`ID`, `in_`, `out_`, `time_`) VALUES (NULL, '62', '55', '2022-07-12 10:39:47.000000');"
           
        # 查詢資料庫

        # cursor = connection.cursor()
        # cursor.execute("SELECT in_ ,out_ ,time_ FROM `flow_people`;")

        # # 列出查詢的資料
        # for (in_, out_,time_) in cursor:
        #     print("in_: %s, out: %s, time: %s" % (in_, out_,time_))

def query(connection):
    # 查詢資料庫

        cursor = connection.cursor()
        cursor.execute("SELECT in_ ,out_ ,time_ FROM `flow_people`;")

        # 列出查詢的資料
        for (in_, out_,time_) in cursor:
            print("in_: %s, out: %s, time: %s" % (in_, out_,time_))


def close_DB(connection):
    if (connection.is_connected()):
        connection.close()
        print("資料庫連線已關閉")


'''  test   '''
# status = conection_DB()
# print(status)
# insert_5min(87,80,str(s),status)
# query(status)
# close_DB(status)


# auto id setting
# alter table hour_count AUTO_INCREMENT=1;
# delete From table_Name 
