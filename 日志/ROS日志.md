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

# 2021.10.29

- 初始化

```c++
/** @brief ROS初始化函数。
 *
 * 该函数可以解析并使用节点启动时传入的参数(通过参数设置节点名称、命名空间...) 
 *
 * 该函数有多个重载版本，如果使用NodeHandle建议调用该版本。 
 *
 * \param argc 参数个数
 * \param argv 参数列表
 * \param name 节点名称，需要保证其唯一性，不允许包含命名空间
 * \param options 节点启动选项，被封装进了ros::init_options
 *
 */
void init(int &argc, char **argv, const std::string& name, uint32_t options = 0);
```
```python
def init_node(name, argv=None, anonymous=False, log_level=None, 
    disable_rostime=False, disable_rosout=False, disable_signals=False, 
    xmlrpc_port=0, tcpros_port=0):
    """
    在ROS msater中注册节点

    @param name: 节点名称，必须保证节点名称唯一，节点名称中不能使用命名空间(不能包含 '/')
    @type  name: str

    @param anonymous: 取值为 true 时，为节点名称后缀随机编号
    @type anonymous: bool
    """
```

- 发布对象

```c++
/**
* \brief 根据话题生成发布对象
*
* 在 ROS master 注册并返回一个发布者对象，该对象可以发布消息
*
* 使用示例如下:
*
*   ros::Publisher pub = handle.advertise<std_msgs::Empty>("my_topic", 1);
*
* \param topic 发布消息使用的话题
*
* \param queue_size 等待发送给订阅者的最大消息数量
*
* \param latch (optional) 如果为 true,该话题发布的最后一条消息将被保存，并且后期当有订阅者连接时会将该消息发送给订阅者
*
* \return 调用成功时，会返回一个发布对象
*
*
*/
template <class M>
Publisher advertise(const std::string& topic, uint32_t queue_size, bool latch = false)
```

```python
class Publisher(Topic):
    """
    在ROS master注册为相关话题的发布方
    """

    def __init__(self, name, data_class, subscriber_listener=None, 
        tcp_nodelay=False, latch=False, headers=None, queue_size=None):
        """
        Constructor
        @param name: 话题名称 
        @type  name: str
        @param data_class: 消息类型

        @param latch: 如果为 true,该话题发布的最后一条消息将被保存，并且后期当有订阅者连接时会将该消息发送给订阅者
        @type  latch: bool

        @param queue_size: 等待发送给订阅者的最大消息数量
        @type  queue_size: int

        """
```

- 回旋函数

在ROS程序中，频繁的使用了 ros::spin() 和 ros::spinOnce() 两个回旋函数，可以用于处理回调函数。

spinOnce():
```c++
/**
 * \brief 处理一轮回调
 *
 * 一般应用场景:
 *     在循环体内，处理所有可用的回调函数
 * 
 */
ROSCPP_DECL void spinOnce();
```
spin():
```c++
/** 
 * \brief 进入循环处理回调 
 */
ROSCPP_DECL void spin();
```
相同点:二者都用于处理回调函数；

不同点:ros::spin() 是进入了循环执行回调函数，而 ros::spinOnce() 只会执行一次回调函数(没有循环)，在 ros::spin() 后的语句不会执行到，而 ros::spinOnce() 后的语句可以执行。

- 时间

1.时刻

获取时刻，或是设置指定时刻:
```c++
// 头文件是 ros.h
ros::init(argc,argv,"hello_time");
ros::NodeHandle nh;//必须创建句柄，否则时间没有初始化，导致后续API调用失败
ros::Time right_now = ros::Time::now();//将当前时刻封装成对象
//时间参考系为：1970年01月01日 00:00:00
ROS_INFO("当前时刻:%.2f",right_now.toSec());//获取距离 1970年01月01日 00:00:00 的秒数
ROS_INFO("当前时刻:%d",right_now.sec);//获取距离 1970年01月01日 00:00:00 的秒数

ros::Time someTime(100,100000000);// 参数1:秒数  参数2:纳秒
ROS_INFO("时刻:%.2f",someTime.toSec()); //100.10
ros::Time someTime2(100.3);//直接传入 double 类型的秒数
ROS_INFO("时刻:%.2f",someTime2.toSec()); //100.30
```
```python
# 获取当前时刻
right_now = rospy.Time.now()
rospy.loginfo("当前时刻:%.2f",right_now.to_sec())
rospy.loginfo("当前时刻:%.2f",right_now.to_nsec())
# 自定义时刻
some_time1 = rospy.Time(1234.567891011)
some_time2 = rospy.Time(1234,567891011)
rospy.loginfo("设置时刻1:%.2f",some_time1.to_sec())
rospy.loginfo("设置时刻2:%.2f",some_time2.to_sec())

# 从时间创建对象
# some_time3 = rospy.Time.from_seconds(543.21)
some_time3 = rospy.Time.from_sec(543.21) # from_sec 替换了 from_seconds
rospy.loginfo("设置时刻3:%.2f",some_time3.to_sec())
```


2.持续时间
```c++
// 设置一个时间区间(间隔):
ROS_INFO("当前时刻:%.2f",ros::Time::now().toSec());
ros::Duration du(10);//持续10秒钟,参数是double类型的，以秒为单位
du.sleep();//按照指定的持续时间休眠
ROS_INFO("持续时间:%.2f",du.toSec());//将持续时间换算成秒
ROS_INFO("当前时刻:%.2f",ros::Time::now().toSec());
```
```python
# 设置一个时间区间(间隔):

# 持续时间相关API
rospy.loginfo("持续时间测试开始.....")
du = rospy.Duration(3.3)
rospy.loginfo("du1 持续时间:%.2f",du.to_sec())
rospy.sleep(du) #休眠函数
rospy.loginfo("持续时间测试结束.....")
```
3.设置运行频率
```c++
ros::Rate rate(1);//指定频率
while (true)
{
    ROS_INFO("-----------code----------");
    rate.sleep();//休眠，休眠时间 = 1 / 频率。
}
```
```python
# 设置执行频率
rate = rospy.Rate(0.5)
while not rospy.is_shutdown():
    rate.sleep() #休眠
    rospy.loginfo("+++++++++++++++")
```
4.定时器

ROS 中内置了专门的定时器，可以实现与 ros::Rate 类似的效果:
```c++
ros::NodeHandle nh;//必须创建句柄，否则时间没有初始化，导致后续API调用失败

 // ROS 定时器
 /**
* \brief 创建一个定时器，按照指定频率调用回调函数。
*
* \param period 时间间隔
* \param callback 回调函数
* \param oneshot 如果设置为 true,只执行一次回调函数，设置为 false,就循环执行。
* \param autostart 如果为true，返回已经启动的定时器,设置为 false，需要手动启动。
*/
 //Timer createTimer(Duration period, const TimerCallback& callback, bool oneshot = false,
 //                bool autostart = true) const;

 // ros::Timer timer = nh.createTimer(ros::Duration(0.5),doSomeThing);
 ros::Timer timer = nh.createTimer(ros::Duration(0.5),doSomeThing,true);//只执行一次

 // ros::Timer timer = nh.createTimer(ros::Duration(0.5),doSomeThing,false,false);//需要手动启动,timer.start();
 // timer.start();

 ros::spin(); //必须 spin

// 定时器的回调函数:

void doSomeThing(const ros::TimerEvent &event){
    ROS_INFO("-------------");
    ROS_INFO("event:%s",std::to_string(event.current_real.toSec()).c_str());
}
```
```python
#定时器设置
"""    
def __init__(self, period, callback, oneshot=False, reset=False):
    Constructor.
    @param period: 回调函数的时间间隔
    @type  period: rospy.Duration
    @param callback: 回调函数
    @type  callback: function taking rospy.TimerEvent 定时器事件
    @param oneshot: 设置为True，就只执行一次，否则循环执行
    @type  oneshot: bool
    @param reset: if True, timer is reset when rostime moved backward. [default: False]
    @type  reset: bool
"""
rospy.Timer(rospy.Duration(1),doMsg)
# rospy.Timer(rospy.Duration(1),doMsg,True) # 只执行一次
rospy.spin()

# 回调函数:

def doMsg(event):
    rospy.loginfo("+++++++++++")
    rospy.loginfo("当前时刻:%s",str(event.current_real))
```

- 其他函数


在发布实现时，一般会循环发布消息，循环的判断条件一般由节点状态来控制，C++中可以通过 ros::ok() 来判断节点状态是否正常，而 python 中则通过 rospy.is_shutdown() 来实现判断，导致节点退出的原因主要有如下几种:

    节点接收到了关闭信息，比如常用的 ctrl + c 快捷键就是关闭节点的信号；

    同名节点启动，导致现有节点退出；

    程序中的其他部分调用了节点关闭相关的API(C++中是ros::shutdown()，python中是rospy.signal_shutdown())

```c++
/** \brief 检查节点是否已经退出
 *
 *  ros::shutdown() 被调用且执行完毕后，该函数将会返回 false
 *
 * \return true 如果节点还健在, false 如果节点已经火化了。
 */
bool ok();

/*
*   关闭节点
*/
void shutdown();
```

```python
def is_shutdown():
    """
    @return: True 如果节点已经被关闭
    @rtype: bool
    """
def signal_shutdown(reason):
    """
    关闭节点
    @param reason: 节点关闭的原因，是一个字符串
    @type  reason: str
    """
def on_shutdown(h):
    """
    节点被关闭时调用的函数
    @param h: 关闭时调用的回调函数，此函数无参
    @type  h: fn()
    """
```

另外，日志相关的函数也是极其常用的，在ROS中日志被划分成如下级别:

    DEBUG(调试):只在调试时使用，此类消息不会输出到控制台；

    INFO(信息):标准消息，一般用于说明系统内正在执行的操作；

    WARN(警告):提醒一些异常情况，但程序仍然可以执行；

    ERROR(错误):提示错误信息，此类错误会影响程序运行；

    FATAL(严重错误):此类错误将阻止节点继续运行。

```c++
ROS_DEBUG("hello,DEBUG"); //不会输出
ROS_INFO("hello,INFO"); //默认白色字体
ROS_WARN("Hello,WARN"); //默认黄色字体
ROS_ERROR("hello,ERROR");//默认红色字体
ROS_FATAL("hello,FATAL");//默认红色字体
```
```python
rospy.logdebug("hello,debug")  #不会输出
rospy.loginfo("hello,info")  #默认白色字体
rospy.logwarn("hello,warn")  #默认黄色字体
rospy.logerr("hello,error")  #默认红色字体
rospy.logfatal("hello,fatal") #默认红色字体
```

- ROS元功能包

