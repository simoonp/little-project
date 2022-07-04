# Exsi安装openwrt作为旁路由

## 前期准备

```shell
 # 用于解压下载
 sudo apt-get -y install gzip
 # 用于将镜像转换为vmdk格式
 sudo apt-get install qemu-utils
```

[原文件(Google Drive)](https://drive.google.com/drive/folders/1o6tJA7aE_TkBRcQmEBlD1twObe0DKBSe)

[所用的固件(百度云) 密码：1111](https://pan.baidu.com/s/1xlCa-hSPp0-khh9q8S3CPg)(用户名：root，密码：netflixcn.com)

```shell
# 解压镜像文件
gunzip openwrt-x86-64-squashfs-combined-D201231-Mask.img.gz
#转换镜像文件
qemu-img convert -f raw -O vmdk openwrt-x86-64-squashfs-combined-D201231-Mask.img openwrt-x86-64-squashfs-combined-D201231-Mask.vmdk
```

## 将转换后的`.vmdk`文件上传到服务的存储中

![image-20220630162437773](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656577478.png)

## 创建虚拟机

![image-20220630162609301](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656577569.png)

选择操作系统

![image-20220630162649569](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656577609.png)

选择可用的存储位置

![image-20220630162728824](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656577648.png)

分配`内存`和`处理器`大小，分配网络(这里的网络是可以直接上网的)，移除硬盘

![image-20220630163557368](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578157.png)

开启Exsi后台的ssh

![image-20220630163855040](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578335.png)

```shell
# ssh登录Exsi
ssh root@xxx.xxx.xxx.xxx
# 切换到刚刚上传的镜像的位置
cd /vmfs/volumes/datastore1/openwrt-image/
# 使用vmkfstools工具将镜像转换为可用的镜像
# vmkfstools -i 原镜像名 新镜像名
vmkfstools -i openwrt-x86-64-squashfs-combined-D201231-Mask.vmdk openwrt_x86_02.vmdk
```

添加刚刚转换的镜像

![image-20220630163626483](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578186.png)

![image-20220630163644264](C:\Users\MOON\AppData\Roaming\Typora\typora-user-images\image-20220630163644264.png)

配置网络适配器类型为`E1000`

![image-20220630163752480](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578272.png)



## 开机

在开机信息不更新后按回车进入`openwrt`

![image-20220630164338802](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578618.png)

使用`vi`修改`IP`，(`vi`用法自行搜索)

```shell
vi /etc/config/network
```

![image-20220630164651798](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656578811.png)

```shell
# 重启网卡
service network restart
# 重启openwrt
reboot
```

## 设置openwrt

根据刚刚设置的静态IP登录openwrt的后台

![image-20220630165010416](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656579010.png)

修改`LAN`口

![image-20220630165058625](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656579058.png)

添加网关

![image-20220630165144390](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656579104.png)

忽略`DHCP服务器`

![image-20220630165518180](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656580567.png)

`保存&应用`

![image-20220630165607232](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/06/upgit_20220630_1656579367.png)

## 同网段下的其他终端设备通过openwrt上网

只需将设备的网关设置为`openwrt`的地址即可

[Ubuntu设置静态IP](https://blog.csdn.net/u014454538/article/details/88646689)

