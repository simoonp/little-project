#! /bin/bash
echo "删除原来的包"
rm -rf gps_ws/

echo "创建工作空间并初始化"
cd ~
mkdir -p gps_ws/src
cd ~/gps_ws
catkin_make

echo "进入 src 创建 ros 包并添加依赖"
cd src
catkin_create_pkg mygps std_msgs rospy roscpp sensor_msgs

echo "安装python功能包"
sudo apt-get install python-requests

sleep 1s

echo "自定义发送的GPS消息类型"

cd ~/gps_ws/src/mygps
mkdir msg
cd msg

echo "创建自定义消息"

#touch myGPS.msg
#echo "uint16 state" >> myGPS.msg
#echo "uint32 deg" >> myGPS.msg
#echo "float64 dis" >> myGPS.msg
#echo "uint32 compass" >> myGPS.msg

#cp ~/tmp/myGPS.msg .

wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/myGPS.msg
cat myGPS.msg

cd ~/gps_ws/src/mygps
echo "修改package.xml"
sed -ri '/<build_depend>std_msgs</ a\  <build_depend>message_generation</build_depend>' package.xml
sed -ri '/<build_export_depend>std_msgs</ a\ a\  <build_export_depend>message_generation</build_export_depend>' package.xml
sed -ri '/<build_export_depend>roscpp/ i\ ' package.xml	# 插入空行
sed -ri '/<exec_depend>std_msgs</ a\  <exec_depend>message_runtime</exec_depend>' package.xml
sed -ri '/<exec_depend>roscpp/ i\ ' package.xml	# 插入空行

echo "修改CMakeLists.txt"
sed -ri '/  rospy/ a\  message_generation' CMakeLists.txt

sed -ri '/# add_message_files/ i\ add_message_files(' CMakeLists.txt
sed -ri '/# add_message_files/ i\   FILES' CMakeLists.txt
sed -ri '/# add_message_files/ i\   myGPS.msg' CMakeLists.txt
sed -ri '/# add_message_files/ i\ )' CMakeLists.txt

sed -ri '/# generate_messages/ i\ generate_messages(' CMakeLists.txt
sed -ri '/# generate_messages/ i\   DEPENDENCIES' CMakeLists.txt
sed -ri '/# generate_messages/ i\   sensor_msgs   std_msgs' CMakeLists.txt
sed -ri '/# generate_messages/ i\ )' CMakeLists.txt

cd ~/gps_ws
catkin_make

echo "消息类型如下"
source ~/gps_ws/devel/setup.bash
rosmsg show myGPS

echo "添加py脚本"
cd ~/gps_ws/src/mygps
mkdir scripts
cd scripts
wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/control.py
wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/mag.py
wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/PID_test.py
wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/net.py
#cp ~/tmp/control.py .
#cp ~/tmp/mag.py .
chmod u+x *.py

echo "添加底层控制程序"
cd ~/gps_ws/src/mygps
cd src
wget https://raw.githubusercontent.com/simoonp/little-project/main/src/gps/ctrl.cpp
#cp ~/tmp/ctrl.cpp .

echo "修改CMakeLists.txt"
cd ..
sed -ri '/# add_executable/ a\add_executable(ctrl src/ctrl.cpp)' CMakeLists.txt
sed -ri '/## Add cmake target dependencies of the executable/ a\add_dependencies(ctrl ${catkin_EXPORTED_TARGETS})' CMakeLists.txt
sed -ri '/# target_link_libraries/ i\target_link_libraries(ctrl ${catkin_LIBRARIES})' CMakeLists.txt

cd ~/gps_ws
echo "重新编译"
catkin_make

sed -i '/gps_w/d' ~/.bashrc # 删除原来的source
echo "source ~/gps_ws/devel/setup.bash" >> ~/.bashrc

