from mysql.connector import connect
import numpy as np

import tracker
from detector import Detector
# from cv2 import cv2
import os
import datetime

#importing libraries
import socket
import cv2
import pickle
import struct
import imutils

# import pyttsx3  
import threading
import time

from connect_DB import *

#  播放聲音 
# send_voice = pyttsx3.init() 


# 建立一個子執行緒

# def job():
#     data1 = f"掰掰下次再來~"  
#     send_voice.say(data1)  
#     send_voice.runAndWait() 
# def job1():
#     data1 = f"歡迎光臨AI中心~~"  
#     send_voice.say(data1)  
#     send_voice.runAndWait()


up = False
h = False
one_up = 0
one_down = 0
status = conection_DB()
# dic = 'C:\\Users\\user\\Desktop\\win10_yolov5_deepsort_counting\\imgs'
if __name__ == '__main__':

    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)

    # 初始化2个撞线polygon
    # list_pts_blue = [[204, 305], [227, 431], [605, 522], [1101, 464], [1900, 601], [1902, 495], [1125, 379], [604, 437], [299, 375], [267, 289]]
    list_pts_blue =  [[700, 500], [1200, 500], [1200, 475], [700, 475]]

    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=1)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]

    # 填充第二个polygon
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
    # list_pts_yellow = [[181, 305], [207, 442], [603, 544], [1107, 485], [1898, 625], [1893, 701], [1101, 568], [594, 637], [118, 483], [109, 303]]
    list_pts_yellow = [[700, 525], [1200, 525], [1200, 550], [700, 550]]

    ndarray_pts_yellow = np.array(list_pts_yellow, np.int32)
    polygon_yellow_value_2 = cv2.fillPoly(mask_image_temp, [ndarray_pts_yellow], color=2)
    polygon_yellow_value_2 = polygon_yellow_value_2[:, :, np.newaxis]

    # 撞线检测用mask，包含2个polygon，（值范围 0、1、2），供撞线计算使用
    polygon_mask_blue_and_yellow = polygon_blue_value_1 + polygon_yellow_value_2

    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (960, 540))

    # 蓝 色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝 polygon图片1
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)

    # 黄 色盘
    yellow_color_plate = [0, 255, 255]
    # 黄 polygon图片
    yellow_image = np.array(polygon_yellow_value_2 * yellow_color_plate, np.uint8)

    # 彩色图片（值范围 0-255）
    color_polygons_image = blue_image + yellow_image
    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (960, 540))

    # list 与蓝色polygon重叠
    list_overlapping_blue_polygon = []

    # list 与黄色polygon重叠
    list_overlapping_yellow_polygon = []

    # 进入数量
    down_count = 0
    # 离开数量
    up_count = 0

    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))

    # 初始化 yolov5
    detector = Detector()


    capture = cv2.VideoCapture(1)

    while True:


    

        # 時間戳記
        s = datetime.datetime.now()
        # [ 2022-07-12 , 10:46:30.740827 ]
        dt = str(s).split(' ')
        #  [10:46:30 ,740827 ]
        d = str(dt[1]).split('.')
        # 10,46,30
        mins = str(d[0]).split(":")
        # 46
        
        
        #資料傳回資料庫
        # ===========================================================================================================================
        
        # # 五分鐘上傳DB
        

        if (int(mins[1]) % 5 ==0 and str(mins[2]) == "00" and up == False):
            insert_5min(down_count,up_count,str(s),status)
            down_count = 0
            up_count = 0
            up = True


        if (int(mins[1]) % 5 != 0  ):
            up = False



        # # 一小時上傳
        if str(mins[1])=="59" and h == False:
           insert_hour(one_down,one_up,str(s),status)
           h = True
           one_down = 0
           one_up = 0

        if str(mins[1])!="59":
            h = False

        
        
        # ===========================================================================================================================
        
        
        # 每幀數
        _, im = capture.read()
        if im is None:
            break

        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))

        list_bboxs = []
        bboxes = detector.detect(im)

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)

            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass

        # 输出图片
        output_image_frame = cv2.add(output_image_frame, color_polygons_image)
        
        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                x1, y1, x2, y2, label, track_id = item_bbox

                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                y1_offset = int(y1 + ((y2 - y1) * 0.6))
                #y1_offset = int(y1 + ((y2 - y1)))

                # 撞线的点
                y = y1_offset
                x = x1

                if polygon_mask_blue_and_yellow[y, x] == 1:
                    # 如果撞 蓝polygon
                    if track_id not in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.append(track_id)
                    pass

                    # 判断 黄polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 外出方向
                    if track_id in list_overlapping_yellow_polygon:
                        
                        # 外出+1
                        up_count += 1
                        one_up += 1
                        # os.chdir(dic)
                        current_time = datetime.datetime.now()
                        # c=str(current_time).split(' ')
                        # t=c[1].split('.')
                        print(current_time)

                        # filename = str(track_id)+'.jpg'
                        # cv2.imwrite(filename, im)
                        # data1 = f"掰掰下次再來~"  
                        # s.say(data1)  
                        # s.runAndWait() 
                        # t = threading.Thread(target = job)
                        # t.start()

                        

                        print(
                            # up 等於出去
                            f'类别: {label} | id: {track_id} | 上行撞线 | 上行撞线总数: {up_count} | 上行id列表: {list_overlapping_yellow_polygon}')

                        # 删除 黄polygon list 中的此id
                        list_overlapping_yellow_polygon.remove(track_id)

                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass

                elif polygon_mask_blue_and_yellow[y, x] == 2:
                    # 如果撞 黄polygon
                    if track_id not in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.append(track_id)
                    pass

                    # 判断 蓝polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 进入方向
                    if track_id in list_overlapping_blue_polygon:
                        # 进入+1
                        down_count += 1
                        one_down += 1
                        # os.chdir(dic)
                        current_time = datetime.datetime.now()
                        print(current_time)
                        # print(current_time+'/'+str(track_id))
                        # c=str(current_time).split(' ')
                        # t=c[1].split('.')

                        # filename = str(track_id)+'.jpg'
                        # cv2.imwrite(filename, im)
                        # data1 = f"歡迎光臨AI中心~~" 
                        # s.say(data1)  

                        # s.runAndWait() 

                        # 建立一個子執行緒
                        # t1 = threading.Thread(target = job1)
                        # t1.start()
   
                        

                        print(
                            #  down 進來
                            f'类别: {label} | id: {track_id} | 下行撞线 | 下行撞线总数: {down_count} | 下行id列表: {list_overlapping_blue_polygon}')

                        # 删除 蓝polygon list 中的此id
                        list_overlapping_blue_polygon.remove(track_id)

                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass
                    pass
                else:
                    pass
                pass

            pass


            # ----------------------清除无用id----------------------
        
            list_overlapping_all = list_overlapping_yellow_polygon + list_overlapping_blue_polygon
            for id1 in list_overlapping_all:
                is_found = False
                for _, _, _, _, _, bbox_id in list_bboxs:
                    if bbox_id == id1:
                        is_found = True
                        break
                    pass
                pass

                if not is_found:
                    # 如果没找到，删除id
                    if id1 in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.remove(id1)
                    pass
                    if id1 in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.remove(id1)
                    pass
                pass
            list_overlapping_all.clear()
            pass

            # 清空list
            list_bboxs.clear()

            pass
        else:
            # 如果图像中没有任何的bbox，则清空list
            list_overlapping_blue_polygon.clear()
            list_overlapping_yellow_polygon.clear()
            pass
        pass
        
        text_draw = 'IN: ' + str(down_count) + \
                    ' , OUT: ' + str(up_count)+ \
                    ' , H_IN: ' + str(one_down)+ \
                    ' , H_OUT: ' + str(one_up)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion,
                                         fontFace=font_draw_number,
                                         fontScale=1, color=(255, 255, 255), thickness=2)
        
        # cv2.namedWindow("demo",0)
        # cv2.resizeWindow("demo", 1920, 1080)
        cv2.imshow('demo', output_image_frame)

        # time2 = time.time()
        # print(time2-time1)
        cv2.waitKey(1)

        pass
    pass

    # capture.release()
    cv2.destroyAllWindows()
    close_DB(status)
