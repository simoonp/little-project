#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
import requests
import json
import time
import datetime
import socket

from std_msgs.msg import String

try:
    import httplib
except:
    import http.client as httplib

def internet_on():
    try:
        html = requests.get("http://www.baidu.com",timeout=(0.5,0.9))
        status = html.status_code
        print( "internet_on 检测有网络")
        print(status)
    except:
        print( "internet_on 检测无网络")
        return 404 #False
    return 200 #True

def have_internet():
    conn = httplib.HTTPConnection("www.baidu.com", timeout=(0.5))
    try:
        conn.request("HEAD", "/")
        conn.close()
        print( "have_internet 检测有网络")
        return 200 #True
    except:
        conn.close()
        print("have_internet 检测无网络")
        return 404 #False

def waitnet2():
    
    #headers={'Connection', 'close'}
    try:
        html = requests.get("http://www.baidu.com",timeout=0.4)
    except:
        return 404
    #return 200
    return html.status_code

def waitnet():
    url="www.baidu.com"
    try:
        host = socket.gethostbyname(url)
        s = socket.create_connection((host, 80), 2)
        return 200 #True
    except Exception as e:
        return 404 #False
if __name__ == "__main__":
    #初始化节点，名称为NetworkMonitoring，用来监视是否连接互联网
    rospy.init_node("NetworkMonitoring")

    #发乎话题 NetMonitor
    pub = rospy.Publisher("NetMonitor",String,queue_size=10)

    msg = String()  #创建 msg 对象
    #msg_front="True"
    count = 0  #计数器

    # 设置循环频率
    rate = rospy.Rate(2)
    
    headers = {'Connection': 'close',}
    while not rospy.is_shutdown():  #当节点没有被杀死时循环
#       print(datetime.datetime.now())
#	have_internet()
#	print(datetime.datetime.now())
#	internet_on()
#	print(datetime.datetime.now())
        status = have_internet()  #状态码，200正常，404异常
#	print(datetime.datetime.now())	
#	print(waitnet2())
#	print(datetime.datetime.now())	
        msg.data = str(status) + '-'+ str(count)

        pub.publish(msg)
        rospy.loginfo("网络状态:%s",msg.data)
        count += 1
        rate.sleep()

