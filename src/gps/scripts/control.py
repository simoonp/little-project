#!/usr/bin/env python
#-*- coding:utf-8 –*-

#2021.10.27 更新,单独接收/gps/fix话题，单独发布路径信息

import math
from re import split
import json
import requests
import rospy
import time

import threading
from rospy.core import rospyinfo    #线程

import tf
from tf.transformations import *
from sensor_msgs.msg import Imu

from sensor_msgs.msg import NavSatFix
from mygps.msg import myGPS
from std_msgs.msg import String
from std_msgs.msg import Float64

#pub = rospy.Publisher('deg_dis', myGPS, queue_size=10)  #发布话题设为全局变量
status = 0
the_location = []
yawdata = 0
net_state=True  # 网络状态
ttmcp = 0   #计次
msg = myGPS()

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

#路线规划，输入参数为起点和终点的经纬度，经纬度数据是gcj02坐标
def route_planning(lon1,lat1,lon2,lat2):
    rospy.loginfo("获取路线")
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

    formatted_url = url + '?' + '&'.join(["{}={}".format(k,v) for k,v in parameters.items()])  # ! # 坐标显示正常
    response = requests.get(formatted_url)
    # print(formatted_url)
    txt = json.loads(response.text)

    global status 
    status = txt['status']

    status = int(status[0])
    #print("status",status)
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
        j=0
        for i in txt:
            i = i['polyline']
            info.append(j)
            j=j+1
            info.append(i)
        rospy.loginfo("路径获取成功")
        status = 1
        return info

#获取点2相对于点1的绝对角度，正北方向为0°，输入参数为两个点的经纬度
def get_degree(lon1,lat1,lon2,lat2):
    rospy.loginfo("获取下一个点的角度-")

    rad=3.1415926535897932384626/180
    
    #角度转弧度
    lat1=lat1*rad
    lon1=lon1*rad
    
    lat2=lat2*rad
    lon2=lon2*rad
    
    a = math.sin(lon2-lon1) * math.cos(lat2)
    b = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)
    
    result = math.atan2(a,b)/rad
    if result<0 :
        result += 360 
    return result

#获取两点之间的距离，单位 m ,输入参数为两个点的经纬度
def get_distance(lon1,lat1,lon2,lat2):
    """
    算法来源：http://developer.baidu.com/map/jsdemo.htm#a6_1
    :param pointA: {lat:29.490295, lng:106.486654}
    :param pointB: {lat:29.615467, lng:106.581515}
    :return:米
    """
    rospy.loginfo("获取下一个点的距离+")

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
    rospy.loginfo("第一条路径数据")
    path=info[1].split(';') #获取第一条路径数据
    data=[]
    # 只使用第一个点
    lon=float(path[0].split(',')[0])
    lat=float(path[0].split(',')[1])
    
    degree = int(get_degree(lon,lat,longitude, latitude))
    distance = get_distance(lon,lat,longitude, latitude)

    data.append(str(degree)+","+str(distance))
    return data[0]

# 判断是否在国内   
def out_of_china(lng, lat):
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

# 判断是否连接互联网 |已弃用， 单独写成一个节点    
def isConnected():
    try:
        html = requests.get("http://www.baidu.com",timeout=2)
    except:
        return False
    return True

# 通过IMU获取偏航角
def callbackYaw(data):
    global yawdata
    error = 0  # 偏移量
    #这个函数是tf中的,可以将四元数转成欧拉角
    (r,p,y) = tf.transformations.euler_from_quaternion((data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w))
    #由于是弧度制，下面将其改成角度制看起来更方便
    #rospy.loginfo("Roll = %f, Pitch = %f, Yaw = %f",r*180/3.1415926,p*180/3.1415926,y*180/3.1415926)
    # yawdata = (0-(y*180/3.1415926 + error ))%360
    yawdata = y*180/3.1415926
    # rospy.loginfo("偏航角：%f", yawdata)

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

# 获取GPS模块的数据
def callbackGPS(gps):
    # if out_of_china(gps.longitude, gps.latitude):
        # the_location = convert(106.606024,29.532828)      
    # else:
        # the_location = convert(gps.longitude,gps.latitude)    #转换为gcj02坐标
    global the_location
    #经度longitude  纬度latitude
    the_location = convert(gps.longitude,gps.latitude)    #转换为gcj02坐标

# 处理数据
def DegDis():
    global ttmcp
    global net_state
    global the_location
    global msg
    global status
    global yawdata

    ttmcp = ttmcp + 1
    rospy.loginfo("%d", ttmcp)
    msg.compass=yawdata
    if net_state == True:   # 网络正常
        #使用 , 分割元素
        # print(the_location)
        longitude=the_location.split(',')[0]
        latitude=the_location.split(',')[1]
        #rospy.loginfo('Listener: GPS: %s %s', (longitude), (latitude))

        rospy.loginfo("目标：南山派出所")
        goal_longitude=106.6023346
        goal_latitude=29.5357341

        info1 = route_planning(longitude,latitude,goal_longitude,goal_latitude)
        #print(info1)
        #print("status",status)
        

        if status != 1 :
            msg.state = status   # 0获取路径失败, 3没有具体的路径
            msg.deg = 0
            msg.dis = 0            
        elif status ==1 :   # 高德地图成功获取路径
            Deg_Dis = datapath(info1, float(longitude), float(latitude))
            msg.state = ttmcp+3
            msg.deg = int(Deg_Dis.split(',')[0])
            msg.dis = float(Deg_Dis.split(',')[1])
        if msg.deg==0:
            msg.compass = 0
        if msg.dis > 5:
            msg.dis = 5

    elif net_state == False:
       # global yawdata
        rospy.loginfo('The network is not connected')
        # msg = myGPS()
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
    """
    sub_imu = rospy.Subscriber('/handsfree/imu', Imu, callbackYaw, queue_size=10)
    sub_net = rospy.Subscriber('/NetMonitor', String, callbackNet, queue_size=10)
    sub_gps = rospy.Subscriber('/gps/fix', NavSatFix, callbackGPS, queue_size=10)
    """
    rospy.Subscriber('/handsfree/imu', Imu, callbackYaw, queue_size=10)
    rospy.Subscriber('/NetMonitor', String, callbackNet, queue_size=10)
    rospy.Subscriber('/gps/fix', NavSatFix, callbackGPS, queue_size=10)
    rospy.Subscriber('/magnetometer', String, callbackMag, queue_size=10)   
    rospy.spin()    # 单线程情况下，程序只执行到这里，然后等待回调，要执行后面的函数需要添加另外一个线程

if __name__ == '__main__':
    rospy.init_node('pylistener', anonymous=True)
    pub = rospy.Publisher('deg_dis', myGPS, queue_size=10)  #发布话题设为全局变量
    rate = rospy.Rate(1)
    add_thread=threading.Thread(target=listener)
    # listener()

    add_thread.start()  # 开启第二个线程
    time.sleep( 2 ) # 等待前几个订阅的话题更新数据
    rospy.loginfo("开启第二个线程------------------------")
    while not rospy.is_shutdown():
        # print(msg)   # 主函数调用全局变量不用global修饰
        print("---while---")
        DegDis()      
        pub.publish(msg)
        rate.sleep()
        # get time
