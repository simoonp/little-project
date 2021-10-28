# 2021.10.22

- rosnode

```shell
$ rosnode ping    #测试到节点的连接状态
$ rosnode list    #列出活动节点
$ rosnode info    #打印节点信息
$ rosnode machine    #列出指定设备上节点
$ rosnode kill    #杀死某个节点
$ rosnode cleanup    #清除不可连接的节点/清除僵尸节点
```

- rostopic

```shell
$ rostopic bw    #显示主题使用的带宽
$ rostopic delay #显示带有 header 的主题延迟
$ rostopic echo  #打印消息到屏幕
$ rostopic find  #根据类型查找主题
$ rostopic hz    #显示主题的发布频率
$ rostopic info  #显示主题相关信息
$ rostopic list  #显示所有活动状态下的主题
$ rostopic list -v #显示所有活动状态下的主题， 获取话题详情(比如列出：发布者和订阅者个数...)
$ rostopic pub  #将数据发布到主题，接调用命令向订阅者发布消息
                # rostopic pub /主题名称 消息类型 消息内容
$ rostopic type  #打印主题类型
```

# 2021.10.28

- rosmsg

rosmsg是用于显示有关 ROS消息类型的 信息的命令行工具。

```shell
$ rosmsg show    #显示消息描述
$ rosmsg info    #显示消息信息
$ rosmsg list    #列出所有消息
$ rosmsg md5    #显示 md5 加密后的消息, 一种校验算法，保证数据传输的一致性
$ rosmsg package    #显示某个功能包下的所有消息
$ rosmsg packages    #列出包含消息的功能包
```

- rosservice

rosservice包含用于列出和查询ROSServices的rosservice命令行工具。

调用部分服务时，如果对相关工作空间没有配置 path，需要进入工作空间调用 source ./devel/setup.bash

```shell
$ rosservice args #打印服务参数
$ rosservice call    #使用提供的参数调用服务
$ rosservice find    #按照服务类型查找服务
$ rosservice info    #打印有关服务的信息
$ rosservice list    #列出所有活动的服务
$ rosservice type    #打印服务类型
$ rosservice uri    #打印服务的 ROSRPC uri
```

- rossrv

rossrv是用于显示有关ROS服务类型的信息的命令行工具，与 rosmsg 使用语法高度雷同。

```shell
$ rossrv show    #显示服务消息详情
$ rossrv info    #显示服务消息相关信息
$ rossrv list    #列出所有服务信息
$ rossrv md5    #显示 md5 加密后的服务消息
$ rossrv package    #显示某个包下所有服务消息
$ rossrv packages    #显示包含服务消息的所有包
```

- rosparam

rosparam包含rosparam命令行工具，用于使用YAML编码文件在参数服务器上获取和设置ROS参数。

```shell
$ rosparam set    #设置参数
$ rosparam get    #获取参数
$ rosparam load    #从外部文件加载参数
$ rosparam dump    #将参数写出到外部文件, rosparam dump 输出文件的路径及名称
$ rosparam delete    #删除参数
$ rosparam list    #列出所有参数
```

