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
# from coordTransform_utils import gcj02_to_wgs84

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
#获取指定地点的经纬度，输入为某个地名
def get_location_x_y(place):
    #place = input("请输入您要查询的地址")
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'key':'2d3d0be8279d05e00314272bfa68734d',
        'address':'%s' % place
    }
    page_resource = requests.get(url,params=parameters)
    text = page_resource.text       #获得数据是json格式
    data = json.loads(text)         #把数据变成字典格式

    location = data["geocodes"][0]['location']
    print(location)
    return location

#使用高德自带的坐标转换，将GPS坐标转换为gcj02坐标，返回 经度，纬度
def convert(lng, lat):
    rospy.loginfo("GPS坐标转换")
    url= 'https://restapi.amap.com/v3/assistant/coordinate/convert'
    location=str(lng)+','+str(lat)
    parameters = {
        'key':'2d3d0be8279d05e00314272bfa68734d',
        'locations':location,
        'coordsys':'gps'
    }
    formatted_url = url + '?' + '&'.join(["{}={}".format(k,v) for k,v in parameters.items()])  # ! # 坐标显示正常
    # print(formatted_url)
    response = requests.get(formatted_url)
    text = response.text 
    data = json.loads(text)
    location = data['locations']
    # print(type(location))

    return location

def route_planning(lon1,lat1,lon2,lat2):
    rospy.loginfo("获取路线")
    global update_flag
    update_flag = 1 # 获取到数据，标志置1，等待第一段路径走完后复位
    from_location=str(lon1)+","+str(lat1)
    to_location=str(lon2)+","+str(lat2)

    #type = input("出行方式（1.公交、2.步行、3.驾车、4.骑行）,请输入数字")
    type = "2"
    url="https://restapi.amap.com"
    if type=="1":
        url = url+ "/v3/direction/transit/integrated"
    elif type=="2":
        url = url + "/v3/direction/walking"
    elif type=="3":
        url = url + "/v3/direction/driving"
    elif type == "4":
        url = url + "/v4/direction/bicycling"
    parameters = {
        'origin': from_location,
        'destination': to_location,
        'key': '2d3d0be8279d05e00314272bfa68734d',
        'extensions':'all',
        'output':'json',
    }

    formatted_url = url + '?' + '&'.join(["{}={}".format(k,v) for k,v in parameters.items()])  #坐标显示正常
    formatted_url="https://restapi.amap.com/v3/direction/walking?origin=106.606157226563,29.53283203125&output=json&destination=106.6024477,29.5357619&extensions=all&key=2d3d0be8279d05e00314272bfa68734d"
    response = requests.get(formatted_url)
    #print(formatted_url)
    # response = "https://restapi.amap.com/v3/direction/walking?origin=106.606157226563,29.53283203125&output=json&destination=106.6024477,29.5357619&extensions=all&key=2d3d0be8279d05e00314272bfa68734d"
    txt = json.loads(response.text)

    global status 
    status = txt['status']

    status = int(status[0])
    #print("status",status)
    homepath = os.environ['HOME']   # 获取用户目录
    if status == 0:
        status = 0
        return 

    elif 'route' not in txt:
        print("error")
        status = 3
        return 

    else:
        txt = txt['route']['paths'][0]['steps']
        info=[]
                    
        # "r" - 只读
        # "a" - 追加 - 会追加到文件的末尾
        # "w" - 写入 - 会覆盖任何已有的内容
        gcj02file = homepath + "/gps_ws/src/mygps/info/gcj02file.txt"
        wgs84file = homepath + "/gps_ws/src/mygps/info/wgs84file.txt"
        print(wgs84file)
        gcj02f = open(gcj02file,"w")
        gcj02f.write("高德 "+str(datetime.datetime.now()))
        gcj02f.write("\n")
        wgs84f = open(wgs84file,"w")
        wgs84f.write("GPS " + str(datetime.datetime.now()))
        wgs84f.write("\n")
        tmp_num=0
        for i in txt:
            i = i['polyline']
            info.append(i)
            tmp_num = tmp_num+1
            gcj02f.write(str(i))
            
            tmp = i.split(';')
            # print("下面是tmp-------------")
            # print (tmp)
            print("---------------")
            # print(len(tmp),"---")
            k=0
            for j in tmp:                
                # print(j)
                wgs=gcj02_to_wgs84(float(j.split(',')[0]),float(j.split(',')[1]))
                wgs=str(wgs[0])+","+str(wgs[1])
                k=k+1
                if k<len(tmp):
                    wgs = wgs + ";"
                wgs84f.write(str(wgs))

            if(tmp_num < len(txt)):
                wgs84f.write("\n")  
                gcj02f.write("\n")
            # elif(tmp_num == len(txt)):
            #     wgs84f.write("------------------------------------")  
            #     gcj02f.write("------------------------------------")
        gcj02f.close()            
        wgs84f.close()            

        #print(msg)
        #print(dir(msg))
        status = 1
        
        return info

#获取点2相对于点1的绝对角度，正北方向为0°，输入参数为两个点的经纬度
def get_degree(lon1,lat1,lon2,lat2):
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
    # if result<0 :
    #     result += 360 
    # print("degree %f", result)
    return -result

#获取两点之间的距离，单位 m ,输入参数为两个点的经纬度
def get_distance(lon1,lat1,lon2,lat2):
    """
    算法来源：http://developer.baidu.com/map/jsdemo.htm#a6_1
    :param pointA: {lat:29.490295, lng:106.486654}
    :param pointB: {lat:29.615467, lng:106.581515}
    :return:米
    """
    #rospy.loginfo("获取下一个点的距离+")

    R = 6370996.81 #球半径

    if (lon1 and lat1 and lon2 and lat2):
        if lat1 == lat2 and lon1 == lon2:
            distance = 0
        else:
            a_lat = lat1 * math.pi / 180
            a_lng = lon1 * math.pi / 180
            b_lng = lon2 * math.pi / 180
            b_lat = lat2 * math.pi / 180
            # print(a_lng,b_lng,a_lat,b_lat)
            distance = R * math.acos(math.sin(a_lat) * math.sin(b_lat) + math.cos(a_lat) * math.cos(b_lat) * math.cos(b_lng - a_lng))
        return distance

#返回第一个路径点的位置，包括 角度(°)和 距离(m)
def datapath(info, longitude, latitude): 
    global last_deg
    global last_dis
    global flag_i
    global path_flag
    #path=info[1].split(';') #获取第一条路径数据
    path=info[path_flag].split(';') #获取第一条路径数据
    print(path)
    data=[]

    # for i in len(path) :
    if flag_i < len(path):
        distance = get_distance(longitude, latitude,float(path[flag_i].split(',')[0]),float(path[flag_i].split(',')[1]))
        if distance < 1: #距离小于1m，认为到达目标点，更新flag_i
            flag_i=flag_i+1
            distance = get_distance(longitude, latitude,float(path[flag_i].split(',')[0]),float(path[flag_i].split(',')[1]))

        degree = get_degree(longitude, latitude,float(path[flag_i].split(',')[0]),float(path[flag_i].split(',')[1]))

        data.append(degree)
        data.append(distance)

    else:  # 走完一段路径，更新下一段路径标志 
        path_flag = path_flag + 1
        flag_i = 0 # 下一段路径第0个点复位
        distance = get_distance(longitude, latitude,float(path[flag_i].split(',')[0]),float(path[flag_i].split(',')[1]))
        degree = get_degree(longitude, latitude,float(path[flag_i].split(',')[0]),float(path[flag_i].split(',')[1]))

        data.append(degree)
        data.append(distance)

    rospy.loginfo("现在是\
第\033[32m%d\033[0m 路径中的\
第\033[32m%d\033[0m 个点,\
前进的角度:\033[32m%f\033[0m距离下一个点的距离:\033[32m%f\033[0m",\
path_flag, flag_i, degree, distance)

    return data


# 通过IMU获取偏航角
def callbackYaw(data):
    global yawdata
    error = 0  # 偏移量
    #这个函数是tf中的,可以将四元数转成欧拉角
    (r,p,y) = tf.transformations.euler_from_quaternion((data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w))
    #由于是弧度制，下面将其改成角度制看起来更方便
    #rospy.loginfo("Roll = %f, Pitch = %f, Yaw = %f",r*180/3.1415926,p*180/3.1415926,y*180/3.1415926)
    # yawdata = (0-(y*180/3.1415926 + error ))%360
    yawdata = y*180/3.1415926 + error
    #rospy.loginfo("IMU数据：%f", yawdata)

# 网络检测
def callbackNet(net):
    # rospy.loginfo("网络状态：%s", net.data)
    status = net.data.split('-')[0]
    status = int(status)
    global net_state

    if status==200 :
        net_state=True
    if status==404 :
        net_state=False
    global IMU_error

    errorfile = os.environ['HOME']+"/gps_ws/src/mygps/info/error"
    data = open(errorfile,"r")
    IMU_error = float(data.read())
    rospy.loginfo("IMU 偏移 %f",IMU_error)
    

# 获取GPS模块的数据
def callbackGPS(gps):
    # if out_of_china(gps.longitude, gps.latitude):
        # the_location = convert(106.606024,29.532828)      
    # else:
        # the_location = convert(gps.longitude,gps.latitude)    #转换为gcj02坐标
    global the_location
    #经度longitude  纬度latitude
    the_location = convert(gps.longitude,gps.latitude)    #转换为gcj02坐标
    #print(type(the_location))
    rospy.loginfo("目前的经纬度%s",str(the_location))
    #将定位数据写入文件
    f = open("localdata.txt","a")
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
    print(status)
    ttmcp = ttmcp + 1
    rospy.loginfo("%d", ttmcp)
    msg.compass=yawdata
    if net_state == True:   # 网络正常
        #使用 , 分割元素
        # print(the_location)
        longitude=the_location.split(',')[0]
        latitude=the_location.split(',')[1]

        #rospy.loginfo("目标：南山派出所")
        goal_longitude= 106.6024477
        goal_latitude= 29.5357619
        global update_fla
        global update_flag
        global info1
        if update_flag == 0:
            
            info1 = route_planning(longitude,latitude,goal_longitude,goal_latitude)
            rospy.loginfo("获取高德数据")
            # info1 存储所有路径的信息，格式：[1,"第1段路径的散点的经纬度信息",2,"第2段路径的散点的经纬度信息",...]
        #print(info1)
        #print("status",status)
        

        if status != 1 :
            msg.state = status   # 0获取路径失败, 3没有具体的路径
            msg.deg = 0
            msg.dis = 0            
        elif status ==1 :   # 高德地图成功获取路径
            Deg_Dis = datapath(info1, float(longitude), float(latitude))

            msg.state = ttmcp+3
            #msg.deg = int(Deg_Dis.split(',')[0])
            #msg.dis = float(Deg_Dis.split(',')[1])
            msg.deg = int(Deg_Dis[0])
            msg.dis = float(Deg_Dis[1])
            print(msg.state,msg.deg,msg.dis,msg.compass)
        if msg.deg==0:
            msg.compass = 0

    elif net_state == False:
        rospy.loginfo('The network is not connected')
        msg.state = 2   # 网络连接失败
        msg.deg = 0
        msg.dis = 0
            
def callbackMag(mag):
    # rospy.loginfo("获取磁力计数据")
    data=mag.data
    mx=data.split(':')[0]
    my=data.split(':')[1]
    mz=data.split(':')[2]
    myaw=data.split(':')[3]
    # print(mx,my,mz,myaw)

# 监听
def listener():
    #Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
    # rospy.Subscriber('/handsfree/imu', Imu, callbackYaw, queue_size=10)
    rospy.Subscriber('/NetMonitor', String, callbackNet, queue_size=10)
    # rospy.Subscriber('/gps/fix', NavSatFix, callbackGPS, queue_size=10)
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
    f = open("localdata.txt","a")
    f.write(str(datetime.datetime.now()))
    f.write("\n")
    f.close()
    gps_i=1.0
    while not rospy.is_shutdown():
        # print(msg)   # 主函数调用全局变量不用global修饰
        global info1
        print("---while---")

        # DegDis()   
        msg.state = gps_i
        msg.plan_flag = 1
        msg.WGS84_lat =  29.5357341  + gps_i/1000000
        msg.WGS84_lon = 106.6023346 + gps_i /1000000
        pub.publish(msg)
        gps_i = gps_i+1
        rate.sleep()
        # break
