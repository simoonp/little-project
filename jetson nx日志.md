- 安装镜像

- 短接 **FC REC** 和 **GND**

![Image](https://raw.githubusercontent.com/simoonp/picture/main/jetson/short1.jpg)

- 安装 jetpack 

```shell
$ sudo apt install nvidia-jetpack
```

- 查看nx底板上40pinGPIO接口的信息：

```shell
$ sudo /opt/nvidia/jetson-io/jetson-io.py
```
![Image](https://raw.githubusercontent.com/simoonp/picture/main/jetson/GPIO1.jpg)

![Image](https://raw.githubusercontent.com/simoonp/picture/main/jetson/GPIO2.jpg)

- 获取NX的功率

参考链接：https://forums.developer.nvidia.com/t/jetson-tx1-ina226-power-monitor-with-i2c-interface/43819

链接中测量的时TX1的功率，涉及的几个文件是：

    /sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_current0_input
    /sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_voltage0_input
    /sys/devices/platform/7000c400.i2c/i2c-1/1-0040/iio_device/in_power0_input

但是NX中，相关的文件，路径不一致，但是文件名是一样的，用 find 在根目录下全局查找，得到9个文件（有0、1、2三个测量通道）

```shell
$ sudo find / -name "in_[a-z]*[0-9]_input" | grep device
```

搜索结果如下：

    find: ‘/proc/6717’: 没有那个文件或目录
    find: ‘/run/user/1000/gvfs’: 权限不够
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power0_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage2_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current1_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage0_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power1_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current2_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage1_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power2_input
    /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current0_input

把几个文件写道脚本里，方便查看：

Measurement.sh：
```shell
#! /bin/bash
# 参考 https://forums.developer.nvidia.com/t/jetson-tx1-ina226-power-monitor-with-i2c-interface/43819
v1=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage0_input)
i1=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current0_input)
p1=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power0_input)

v2=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage1_input)
i2=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current1_input)
p2=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power1_input)

v3=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_voltage2_input)
i3=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_current2_input)
p3=$(cat /sys/devices/c250000.i2c/i2c-7/7-0040/iio:device0/in_power2_input)

echo "--------"
echo "通道0的电压为: $v1 mV"
echo "通道0的电流为: $i1 mA"
echo "通道0的功率为: $p1 mW"
echo "--------"
echo "通道1的电压为: $v2 mV"
echo "通道1的电流为: $i2 mA"
echo "通道1的功率为: $p2 mW"
echo "--------"
echo "通道2的电压为: $v3 mV"
echo "通道2的电流为: $i3 mA"
echo "通道2的功率为: $p3 mW"
echo "--------"
echo "总功率为 $((p1+p2+p3)) mV"
```

- Jetson监控工具——jtop

```shell
# 前提： 已安装Jetpack
$ sudo pip3 install jetson-stats

# 执行
$ sudo jtop
```