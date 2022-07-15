# HomeKit红外遥控器

项目参考链接：

[esp-homekit-ac-remote](https://github.com/LeeLulin/esp-homekit-ac-remote)

[在Docker中使用 esp-open-sdk](https://leelulin.xyz/2020/10/06/docker-esp/)

[格力空调红外编码解析](https://blog.csdn.net/weixin_44821644/article/details/108704768)

[格力空调 YAPOF3 红外编码](https://snowstar.org/2022/02/21/gree-yapof3-ir-format/)

[格力空调YB0F2红外码]([格力空调遥控器红外编码透析（长码） - 开发者知识库 (itdaan.com)](https://www.itdaan.com/blog/2015/09/02/ce4440e0e983e4f88ab8ff2297877f82.html#:~:text=格力空调遥控器（YB0F2）红外码组成如下，按解码顺序排列 起始码（S）%2B35位数据码%2B连接码（C）%2B32位数据码 1、各种编码的电平宽度：,数据码由“0”“1”组成： 0的电平宽度为：600us低电平%2B600us高电平， 1的电平宽度为：600us低电平%2B1600us高电平))

[IRRemoteESP8266](https://github.com/crankyoldgit/IRremoteESP8266)

## 前期准备

### 安装Docker

按照官网操作即可[Docker 安装](https://docs.docker.com/get-docker/)

### 运行Docker容器

```shell
# 下载镜像
docker pull jedie/esp-open-sdk

# git 代码,将代码放在Downlaod目录下
cd ~/Downlaod
git clone https://github.com/LeeLulin/esp-homekit-direct.git
cd esp-homekit-direct/devices
git clone https://github.com/LeeLulin/esp-homekit-ac-remote.git
# 修改 config.h 中的 wifi 配置
cd esp-homekit-ac-remote
vim config.h
#define WIFI_SSID "ssid name"
#define WIFI_PASS "password"

# 新建容器,并将ttyUSB0挂载到容器上, 根据具体情况看是哪个USB接口
docker run -it --name esp --device=/dev/ttyUSB0:/dev/ttyUSB0 jedie/esp-open-sdk:latest /bin/bash

# 进入已启动的容器
docker exec -it esp /bin/bash

# 新开终端,拷贝下载的文件到容器中
docker cp ~/Downlaod/esp-homekit-direct esp:/opt/

# 先输入红外解码固件 raw_dumper.bin 
# 切换到刚刚新建的容器的终端
cd /opt/esp-homekit-direct/devices/esp-homekit-ac-remote/firmware
# 擦除FLASH
esptool.py --port /dev/ttyUSB0 erase_flash
# 刷入固件
esptool.py -p /dev/ttyUSB0 -b 115200 write_flash -fs 8m -fm dout -ff 40m 0x0 rboot.bin 0x1000 blank_config.bin 0x2000 raw_dumper.bin
```

### ESP8266的引脚定义

红外接收：GPIO12(D6)
红外发射：GPIO14(D5)
DHT11温湿度传感器：GPIO4(D2)

## YB0F2红外编码

格力空调遥控器（YB0F2）红外码组成如下，按解码顺序排列 

起始码（S）+35位数据码+连接码（C）+32位数据码 



1、各种编码的电平宽度： 

数据码由**0**，**1**组成： 

0 的电平宽度为：**600us**低电平+**600us**高电平，

1 的电平宽度为：**600us**低电平+**1600us**高电平

起始码S电平宽度为：**9000us**低电平+**4500us**高电平

连接码C电平宽度为：**600us**低电平+**20000us**高电平



 2、数据码的形成机制 

### 前35位数据码形成如下图所示：

![image-20220715094840875](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/07/upgit_20220715_1657849721.png)

1-3位：**模式**

|          | 自动 | 制冷 | 加湿 | 送风 | 制热 |
| -------- | ---- | ---- | ---- | ---- | ---- |
| 模式标志 | 000  | 100  | 010  | 110  | 001  |

4位：**电源**

|开机|关机|
|-------|-------|
|1|0|

5-6位：**风速**

|          | 自动 | 1级  | 2级  | 3级  |
| -------- | ---- | ---- | ---- | ---- |
| 风速标志 | 00   | 10   | 01   | 11   |

7位：**扫风** 

|开启|关闭|
|-------|-------|
|1|0|

8位：**睡眠**

|睡眠|不睡眠|
|-------|-------|
|1|0|

9-12位：**温度**

|  温度  | 16° | 17°  | 18-29°  | 30°  |
| -------- | ---- | ---- | ---- | ---- |
| 编码 | 0000   | 1000   | 逆序递增   | 0111   |

*逆序递增:* $设置温度 - 基础温度(16°) \rightarrow 差值转换为二进制\rightarrow 二进制逆序$

$26 - 10 \rightarrow 10 \rightarrow 1010 \rightarrow 0101$

13-20位：**定时**

21位：**超强**?

| 超强 | 普通 |
| ---- | ---- |
| 1    | 0    |

23位：**健康/负离子**

24位：**干燥/辅热**

25位：**换气**

26-35位：**固定数值,功能未知**

### 后32位数据码形成如下图所示：

![image-20220715094910285](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/07/upgit_20220715_1657849750.png)

36位：**上下扫风**

| 开   | 关   |
| ---- | ---- |
| 1    | 0    |

40位：**左右扫风**

| 开   | 关   |
| ---- | ---- |
| 1    | 0    |

44-45位：**温度显示**

| 不显示 | 显示 | 显示室内温度 | 显示室外温度 |
| ------ | ---- | ------------ | ------------ |
| 00     | 10   | 01           | 11           |

62位：**节能**

54-67位：**校验码***

校验码 = (模式 – 1) + (温度– 16) + 5  + 左右扫风 + 换气 + 节能 - 开关
之后取二进制后四位，再逆序；

**关联规则**
（1）自动模式下，只可以设置的项目有：风速1、2、3级、自动；上上下左右扫风；显示温度；灯光；睡眠定时（非睡眠）。其他项均不可以设置。此时温度不可设置，温度段的代码为：10011101。
（2）关机状态下，可以设置定时开机，代码与睡眠定时关机一样。也可以设置灯光。
（3）制冷模式下，可以设置的项有：温度；扫风；健康换气，节能（仅在此状态下可以设置）；风速；定时；超强；睡眠；灯光；温度显示。
（4）除湿模式下，可以设置的项有：温度；扫风；健康换气；干燥；温度显示；定时；睡眠；灯光。
（5）通风模式下，可以设置的项有：温度；风速；健康换气；扫风；温度显示；定时；灯光。
（6）制热模式下，可以设置的项有：温度；风速；扫风；辅热；温度显示；定时；超强；睡眠；灯光。

## 红外解码

将ESP8266刷入`raw_dumper.bin`固件后，拔掉,重新插在电脑上(windows上的串口助手比较多)

将遥控器对准红外接收器,发送指令

下图是我发送关机指令(`格力空调`)对应的红外码(ESP8266接收到的是2段红外数据,有的一段红外数据)

![image-20220715145309474](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/07/upgit_20220715_1657867989.png)

不同空调的红外解码又区别

手里的`格力`空调对应的是`35+32`数据码格式,但是我不明白为啥会发2段,有可能是我用的是手机自带的红外遥控器的问题

同样的指令,由于红外接收器有误差,电平持续实现会有些许不同,为了方便观察,将接收的红外码格式化,并转换位`0` `1`电平

0 的电平宽度为：**600us**低电平+**600us**高电平，

1 的电平宽度为：**600us**低电平+**1600us**高电平

起始码S电平宽度为：**9000us**低电平+**4500us**高电平

连接码C电平宽度为：**600us**低电平+**20000us**高电平

|| 数据`0` | 数据`1` | 起始码 | 连接码 |
|------| ------- | ------- | ------ | ------ |
|低电平(us)| 600 | 600 | 9000 | 600 |
|高电平(us)| 600 | 1600 | 4500 | 20000 |

会发现$(起始码+35+连接码+32)*2=138$,而实际一组接收了139个数据,有网友说最后的那个代表`结束码`，即:**600us**低电平+高电平，但没说高电平持续了多长时间,暂且设置位`1000us`

实际测试中,高低电平的持续时间有差异,不过不影响

转换测试代码代码:

```C
/*********************************
Author: Simoonp	                 *
Date:   2022-07-14-7月-11:04:28  *
trans.cpp
*********************************/
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;
int data_0_l=680;
int data_0_h=-516;

int data_1_l=data_0_l;
int data_1_h=-1640;

int start_l=9050;
int start_h=-4500;

int and_l = data_0_l;
int and_h = -20000;

int end_l = data_0_l;
int end_h = -1000;

// 格式化
int format(int val){
	if(val>8000 && val<10000)	// start_l
		val = start_l;
	else if(val>-6000 && val<-3000)	//start_h
		val = start_h;
	else if(val>500 && val<800)	//data_0_l
		val = data_0_l;
	else if(val>-700 && val<-400)	//data_0_h
		val=data_0_h;
	else if(val>-1800 && val<-1400)	//data_1_h
		val=data_1_h;
	else if(val<-18000 && val>-22000)	//and_h
		val=and_h;
	return val;
}

int main()
{
	// 串口接收的数据放到 data 文件中,程序会读取原始数据
	ifstream ifs;
	ifs.open("data", ios::in);
	if(!ifs.is_open()){
		cout <<"打开失败"<<endl;
		return 0;
	}
	string buff;
	vector<int> num;
	int tmp=0;
	while(ifs >> buff){
		if(buff == "int16_t"){
			cout << endl;
		}
		if(buff.find(':')>0 && buff.find(':')<20) // 过滤掉串口消息中的统计数
			continue;

		if((buff[0]>='0' && buff[0]<='9') || buff[0]=='-'){	// 筛选出数字
			// cout << buff << " ";
			// tmp++;
		}else
			continue;

		buff.pop_back();	// 去除 最后的 , 字符
		cout << buff << ", ";	// 打印读取的原始数据
		int data = format(stoi(buff)); // 将读取的字符串格式化位数字
		num.push_back(data);	// 存放到num中
	}
	ifs.close();
	cout << endl;
	cout << "共计 " <<num.size() << " 个数字"<< endl;
    // 打印格式化后的数据
	for(int i=0;i<num.size();i++){
		if(i >0 && num[i]==start_l && num[i-1]==end_l){
			cout << endl;
		}
		cout << num[i] << ", ";
	}
	cout << endl;
	//------------------------数据处理---将电平数据转换位0 1 数据,方便观察----------
	vector<char> Logic_type;
	for(int i=0; i<num.size(); i=i+2){
		int log_data;
		if(num[i]==start_l && num[i+1]==start_h){
			Logic_type.push_back('s');
		}else if(num[i]==data_0_l && num[i+1]==data_0_h){
			log_data = 0;
			Logic_type.push_back('0');
		}else if(num[i]==data_1_l && num[i+1]==data_1_h){
			log_data = 1;
			Logic_type.push_back('1');
		}else if(num[i]==and_l && num[i+1]==and_h){
			Logic_type.push_back('-');
		}else if(num[i]==end_l){
			cout << "结束" << endl;
			Logic_type.push_back('e');
			i--;
		}
	}
	// 打印 0 1 的数据
	for(int i=0; i<Logic_type.size(); i++){
		cout << Logic_type[i];
		if(Logic_type[i]=='e')
			cout << endl;
		else 
			cout << " ";
	}

	// 开始写入文件, 将解析的 0 1 数据写入到 logic 文件中
	ofstream out;
	out.open("logic", ios::out|ios::app);
	if(!out.is_open()){
		cout <<"打开失败"<<endl;
		return 0;
	}else{
		out << endl;
		for(int i=0; i<Logic_type.size(); i++){
			out << Logic_type[i] ;
			if(Logic_type[i]=='e')
				out << endl;
			else
				out << " ";
		}
		out << endl;
	}
	out.close();

	// 开始写入格式化的红外数据
	ofstream out_IR;
	out_IR.open("IR_data", ios::out|ios::app);
	if(!out_IR.is_open()){
		cout <<"打开失败"<<endl;
		return 0;
	}else{
		// out_IR << "[" << Logic_type.size()*2 << "] = { ";
		out_IR << "[" << " " << "] = { ";

		for(int i=0; i<Logic_type.size(); i++){
			if(Logic_type[i] == 's'){
				out_IR << start_l << ", " << start_h << ", ";
			}else if(Logic_type[i] == '0'){
				out_IR << data_0_l << ", " << data_0_h << ", ";
			}else if(Logic_type[i] == '1'){
				out_IR << data_1_l << ", " << data_1_h << ", ";
			}else if(Logic_type[i] == '-'){
				out_IR << and_l << ", " << and_h << ", ";
			}else if(Logic_type[i] == 'e'){
				out_IR << end_l << ", " ;
				if(i==Logic_type.size()-1)
					out_IR << "};" <<endl;
				else
					out_IR << ", ";
			}
		}
	}
	out_IR.close();
	return 0;
}
```

## 修改ir.c文件

根据获得的红外数据, 修改`ir.c`中不同的指令对应的红外数据,

```shell
# 刚刚下载的代码中修改ir.c
cd ~/Downlaod/esp-homekit-direct/devices/esp-homekit-ac-remote
vim ir.c

# 将修改后的ir.c文件拷贝到容器中
docker cp ir.c esp02:/opt/esp-homekit-direct/devices/esp-homekit-ac-remote

# 切换到容器的那个终端
cd /opt/esp-homekit-direct
make -C devices/esp-homekit-ac-remote all
# 编译结束后,会在 /opt/esp-homekit-direct/devices/esp-homekit-ac-remote/firmware 目录下生成 cooler.bin文件

# 换一块ESP8266, 主要是方便测试,之后还要可能要同时收发红外数据
# 擦除FLASH
esptool.py --port /dev/ttyUSB0 erase_flash
# 刷入固件
esptool.py -p /dev/ttyUSB0 -b 115200 write_flash -fs 8m -fm dout -ff 40m 0x0 rboot.bin 0x1000 blank_config.bin 0x2000 cooler.bin
```

## 手机/iPad连接ESP8266

参考[手机/iPad连接ESP8266](https://leelulin.xyz/2020/03/16/esp-homekit-03/)

### 发现的问题

将获取的红外数据/格式化后的红外数据复制到ir.c后, 再次接收的数据和代码中的红外数据不一致, 缺少几位数据, 有可能是工程中的红外处理部分的问题, 比较块的修改方法就是手动补全缺失的部分, 再重新收发测试, 缺啥补啥



```C
/*********************************
Author: Simoonp	                 *
Date:   2022-07-14-7月-11:04:28  *
log_2_ir.cpp 将 0 1 数据信号(s 35位数据 - 32位数据 e)转换位红外电平信号
*********************************/
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;
int data_0_l=646;
int data_0_h=-516;

int data_1_l=data_0_l;
int data_1_h=-1640;

int start_l=9050;
int start_h=-4500;

int and_l = data_0_l;
int and_h = -20000;

int end_l = data_0_l;
int end_h = -1000;


void out_ir(string s){
	if(s == "s"){
		cout << start_l <<", " << start_h<< ", ";
	}else if(s == "0"){
		cout << data_0_l <<", " << data_0_h << ", ";
	}else if(s == "1"){
		cout << data_1_l <<", " << data_1_h<< ", ";
	}else if(s == "-"){
		cout << and_l <<", " << and_h<< ", ";
	}else if(s == "e"){
		cout << end_l <<", " << end_h<< ", ";
	}
}
int main()
{	ifstream ifs;
	ifs.open("log", ios::in);
	if(!ifs.is_open()){
		cout <<"打开失败"<<endl;
		return 0;
	}
	string buff;
	vector<int> num;
	int tmp=0;
	while(ifs >> buff){
		// cout << buff << ", ";
		out_ir(buff);
		if(buff == "e"){
			cout << endl;
			continue;
		}
	}
	ifs.close();
	cout << endl;

	return 0;
}
```

