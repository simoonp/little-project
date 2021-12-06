#!/usr/bin/env python
#-*- coding:utf-8 –*-
# 待完成
# 更新思路:只在起点的时候连接高德获取一次全局路径，以后每走完一小段路径，调用存储数据的下一段路径的信息

"""
gps导航一直出问题，可能的原因：GPS的WGS84坐标系转换为国内的火星坐标系(GCJ02)后，由于不是线性变换，
导致，GCJ02上的散点坐标转换回GPS坐标后，
假如散点是在一条直线上的，通过角度/距离算法(基于GPS坐标)，得到的结果不是在一条线上

GPS坐标 --非线性偏移--> GCJ02坐标 --高德API--> 一系列GCJ02坐标
在一条直线上的GPS坐标散点 --非线性偏移--> GCJ02坐标 --角度/距离算法(基于GPS坐标)--> 散点的GCJ02坐标映射在GPS坐标下后，不在一条直线上

2021.11.26-2021.11.28
修改：
    1、更新myGPS.msg
    2、只调用convert()一次，用于获取全局路径规划
    3、只调用route_planning()一次，将返回的所有经纬度坐标点保存到gcj02file.txt中
        将上一次的gcj02file.txt追加到gcj02file.log中
        将高德返回的所有经纬度坐标转换为 WGS08坐标 ，并保存到wgs84file.txt中
        将上一次的wgs84file.txt追加到wgs84file.log中
        获取路径成功后，plan_flag标志位置 True， rviz_pub程序的view节点开始可视化工作
    4、改为用 WGS08坐标 获取角度 和 距离
    5、将每次获取的 WGS08坐标 保存到 localdata.txt 中
    6、添加 IMU 偏移量，修改 error 文件的值，每次发布检查网数据前络的时候程序会读取 error 文件中的值

"""
import math
from re import split
import json
import requests
import rospy
import time
import datetime

import os

import threading
from rospy.core import rospyinfo    #线程

import tf
from tf.transformations import *
from sensor_msgs.msg import Imu

from sensor_msgs.msg import NavSatFix
from mygps.msg import myGPS
from std_msgs.msg import String
from std_msgs.msg import Float64
# from coordTransform_py import coordTransform_util
from coordTransform_utils import gcj02_to_wgs84

#pub = rospy.Publisher('deg_dis', myGPS, queue_size=10)  #发布话题设为全局变量
status = 0
the_location = "0,0"
yawdata = 0
net_state=True  # 网络状态
ttmcp = 0   #计次
msg = myGPS()
last_deg = 0.0
last_dis = 0.0
flag_i = 0  #代表下一个目标点是一段路径中的第i个点
update_flag = 0 # 高德地图数据更新标志，每一小段路径走完后，更新高德地图
path_flag = 0 # 第 i 段路径标志
IMU_error = 0.0

# 读取文件获得数据
def route_planning():
    rospy.loginfo("读取文件")
    global update_flag
    global msg
    msg.state = 1
    msg.plan_flag = True
    update_flag = 1 # 获取到数据，标志置1，等待第一段路径走完后复位
    homepath = os.environ['HOME']   # 获取用户目录
    pathfile = homepath + "/gps_ws/src/mygps/info/path"
    f = open(pathfile, "r")
    data = f.read()
    info = data.split("\r\n")    
    f.close()
    return info

#获取点2相对于点1的绝对角度，正北方向为0°，输入参数为两个点的经纬度
#  目标点经纬度  当前点经纬度
def get_degree(lon2,lat2,lon1,lat1):
    #rospy.loginfo("获取下一个点的角度-")

    rad=3.1415926535897932384626/180
    
    #角度转弧度
    lat1=lat1*rad
    lon1=lon1*rad
    
    lat2=lat2*rad
    lon2=lon2*rad
    
    a = math.sin(lon2-lon1) * math.cos(lat2)
    b = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)
    
    result = math.atan2(a,b)/rad

    return -result

#获取两点之间的距离，单位 m ,输入参数为两个点的经纬度
def get_distance(lon1,lat1,lon2,lat2):
    R = 6370996.81 #球半径

    if (lon1 and lat1 and lon2 and lat2):
        if lat1 == lat2 and lon1 == lon2:
            distance = 0
        else:
            a_lat = lat1 * math.pi / 180
            a_lng = lon1 * math.pi / 180
            b_lng = lon2 * math.pi / 180
            b_lat = lat2 * math.pi / 180
            distance = R * math.acos(math.sin(a_lat) * math.sin(b_lat) + math.cos(a_lat) * math.cos(b_lat) * math.cos(b_lng - a_lng))
        return distance

#返回第一个路径点的位置，包括 角度(°)和 距离(m)
def datapath(longitude, latitude): 
    rospy.loginfo("进入 datapath")
    global info1
    global flag_i
    global msg
    if flag_i >= len(info1):
        msg.state = 2
        rospy.loginfo("导航结束")
        return 

    GPSdata=info1[flag_i].split(',') #获取第 path_flag 数据

    lon = float(GPSdata[0])
    lat = float(GPSdata[1])
    data=[]

    distance = get_distance(lon ,lat , longitude, latitude)
    degree = get_degree(lon ,lat , longitude, latitude)
    data.append(degree)
    data.append(distance)
    if distance < 1.5:
        flag_i = flag_i+1

    rospy.loginfo("现在是\
第\033[32m%d\033[0m 个点,\
前进的角度:\033[32m%f\033[0m距离下一个点的距离:\033[32m%f\033[0m",\
flag_i, degree, distance)
    rospy.loginfo("目标点的经纬度是： %f ， %f", longitude, latitude)
    return data


# 通过IMU获取偏航角
def callbackYaw(data):
    global yawdata
    global IMU_error  # 偏移量
    #这个函数是tf中的,可以将四元数转成欧拉角
    (r,p,y) = tf.transformations.euler_from_quaternion((data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w))
    #由于是弧度制，下面将其改成角度制看起来更方便
    #rospy.loginfo("Roll = %f, Pitch = %f, Yaw = %f",r*180/3.1415926,p*180/3.1415926,y*180/3.1415926)
    # yawdata = (0-(y*180/3.1415926 + error ))%360
    yawdata = y*180/3.1415926 + IMU_error
    #rospy.loginfo("IMU数据：%f", yawdata)

# 获取GPS模块的数据
def callbackGPS(gps):

    global the_location
    global msg
    #经度longitude  纬度latitude
    # 注-- 使用GPS计算角度和距离，不用 gcj02坐标
    # 更新 GPS坐标
    msg.WGS84_lat = float(gps.latitude)
    msg.WGS84_lon = float(gps.longitude)
    the_location = str(gps.longitude)+","+str(gps.latitude)
    rospy.loginfo("目前的经纬度%s",str(the_location))
    #将WGS84数据写入文件
    localfile = os.environ['HOME']+"/gps_ws/src/mygps/info/localdata.txt"
    f = open(localfile,"a")
    f.write(str(the_location))
    f.write("\n")            
    f.close() 

# 处理数据
def DegDis():
    global ttmcp
    global net_state
    global the_location
    global msg
    # global status
    global yawdata
    global flag_i
    rospy.loginfo("+++++进入DegDis++++")
    ttmcp = ttmcp + 1
    msg.compass=yawdata

    # 读取 error 文件
    global IMU_error
    errorfile = os.environ['HOME']+"/gps_ws/src/mygps/info/error"
    try:
        data = open(errorfile,"r")
        IMU_error = float(data.read())
        rospy.loginfo("IMU 偏移 %f",IMU_error)
    finally:
        if data:
            data.close()

    if net_state == True:   # 网络正常
        msg.net_flag = True
        longitude=msg.WGS84_lon
        latitude =msg.WGS84_lat

        global update_fla
        global update_flag
        global info1

        if update_flag == 0:
            
            info1 = route_planning()
            rospy.loginfo("开始读取文本")  

        # if msg.state == 1 :   # 成功获取路径
        Deg_Dis = datapath(float(longitude), float(latitude))
        if msg.state == 1 :   # 成功获取路径
            # flag_i = flag_i+1;
            msg.WGS84_lon = float(longitude)
            msg.WGS84_lat = float(latitude)

            msg.deg = int(Deg_Dis[0])
            msg.dis = float(Deg_Dis[1])

        elif msg.state==2:
            msg.deg = 0
            msg.dis = 0
            msg.compass = 0

            
def callbackMag(mag):
    # rospy.loginfo("获取磁力计数据")
    data=mag.data
    mx=data.split(':')[0]
    my=data.split(':')[1]
    mz=data.split(':')[2]
    myaw=data.split(':')[3]

# 监听
def listener():
    #Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
    rospy.Subscriber('/handsfree/imu', Imu, callbackYaw, queue_size=10)
    rospy.Subscriber('/gps/fix', NavSatFix, callbackGPS, queue_size=10)
    #rospy.Subscriber('/magnetometer', String, callbackMag, queue_size=10)   
    rospy.spin()    # 单线程情况下，程序只执行到这里，然后等待回调，要执行后面的函数需要添加另外一个线程

if __name__ == '__main__':
    rospy.init_node('pylistener', anonymous=True)
    pub = rospy.Publisher('deg_dis', myGPS, queue_size=10)  #发布话题设为全局变量
    rate = rospy.Rate(1)
    add_thread=threading.Thread(target=listener)

    add_thread.start()  # 开启第二个线程
    time.sleep( 2 ) # 等待前几个订阅的话题更新数据
    rospy.loginfo("开启第二个线程------------------------")
    localfile = os.environ['HOME']+"/gps_ws/src/mygps/info/localdata.txt"
    f = open(localfile,"a")
    f.write(str(datetime.datetime.now()))
    f.write("\n")
    f.close()
    # global msg
    msg.state = 1
    while not rospy.is_shutdown():
        global info1
        rospy.loginfo("--------------------while-------------------")
        DegDis()      
        pub.publish(msg)
        rate.sleep()
        # break
