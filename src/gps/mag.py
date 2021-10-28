#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
import time
import serial #导入serial包
import datetime
from std_msgs.msg import String

def send(rev):
    Magx=rev.split(',')[0]
    Magy=rev.split(',')[1]
    Magz=rev.split(',')[2]
    Yaw =rev.split(',')[3]

    Magx=Magx.split(':')[1]
    Magy=Magy.split(':')[1]
    Magz=Magz.split(':')[1]
    Yaw =Yaw.split(':')[1] 

    Magx = int(Magx)*13
    Magy = int(Magy)*13
    Magz = int(Magz)*13
    rospy.loginfo("magx:%f magy:%f magz:%f yaw:%s", Magx*0.00001, Magy*0.00001, Magz*0.00001, Yaw)
    data = str(Magx)+":"+str(Magy)+":"+str(Magz)+":"+str(Yaw)
    
    return data

if __name__ == '__main__':
    rospy.init_node("Mag") #初始化ros节点
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1) #打开串口, 端口号:"/dev/ttyUSB0". 波特率:9600. 延时等待1s
    if ser.isOpen(): #判断串口是否打开
        print("串口打开成功")
    else:
        print("串口打开失败")
        quit()
    pub = rospy.Publisher('magnetometer', String , queue_size=10)  #发布话题

    rate = rospy.Rate(10)   #频率10Hz

    while not rospy.is_shutdown():
        # print("1-------------------------------")
        print(datetime.datetime.now())
        ser.write('AT+PRATE=0\r\n')
        cnt = ser.inWaiting() #等待接受数据
        rev0 = ser.read(cnt) #读数
        rev=rev0.split()    #按换行分割数据

        if len(rev) == 2 :
            print rev[1]
            print("\033[32m数据符合\033[0m")
            if rev[0]=='OK' :
                data = send(rev[1])
                pub.publish(data)
                print("--over--")
            elif rev[1]=='OK':
                data = send(rev[0])
                pub.publish(data)
                print("--over--")

        rate.sleep()
