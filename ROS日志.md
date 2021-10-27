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

- 