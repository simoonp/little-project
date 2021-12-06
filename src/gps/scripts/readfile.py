#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy
import requests

import socket
import os

homepath = os.environ['HOME']   # 获取用户目录
pathfile = homepath + "/gps_ws/src/mygps/info/path"

f = open(pathfile, "r")
data = f.read()
info = data.split("\r\n")
f.close()
print (info)
i = 0
j = 0
# for i in data:
#     print(j , "-", i)
#     j = j+1
while i < len(info):
    # if i%37 ==0:
    #     print(info[i])
    print((info[i].split(',')[0]))
    i = i+1