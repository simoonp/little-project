#include <iostream>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Quaternion.h>
//#include <riki_msgs/myGPS.h>
#include <mygps/myGPS.h>
#include <cmath>



#include <ros/ros.h>
#include <string>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>


using namespace std;

#define _USE_MATH_DEFINES
#define KP 0.2

ros::Subscriber gps_sub;	//订阅gps话题
float gps_d=10;
float gps_t=10;

ros::Subscriber odom_sub;	//订阅odom话题
geometry_msgs::Quaternion odom_quat;

ros::Publisher vel_pub;		//发布速度话题
geometry_msgs::Twist vel;


//四元数数据结构
struct Quaternion {
    double w, x, y, z;
};
//欧拉角数据结构
struct EulerAngles {
    double roll, pitch, yaw;
};

EulerAngles Eul;	//定义欧拉角结构体，用于接受将四元数转换为欧拉角的函数返回值

//四元数转欧拉角函数
EulerAngles ToEulerAngles(geometry_msgs::Quaternion q) {
	// EulerAngles ToEulerAngles(Quaternion q) {
    EulerAngles angles;

    // roll (x-axis rotation) 横滚
    double sinr_cosp = 2 * (q.w * q.x + q.y * q.z);
    double cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y);
    angles.roll = std::atan2(sinr_cosp, cosr_cosp);

    // pitch (y-axis rotation) 俯仰
    double sinp = 2 * (q.w * q.y - q.z * q.x);
    if (std::abs(sinp) >= 1)
        angles.pitch = std::copysign(M_PI / 2, sinp); // use 90 degrees if out of range
    else
        angles.pitch = std::asin(sinp);

    // yaw (z-axis rotation) 偏航(偏向)
    double siny_cosp = 2 * (q.w * q.z + q.x * q.y);
    double cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z);
    angles.yaw = std::atan2(siny_cosp, cosy_cosp);
    
    return angles;
}

//pid算法，可以使机器人转指定角度.参1为欧拉角，参2为gps角度，参3为gps距离
float pid(EulerAngles ang, float gpsdeg,float gpsdis)
{
	setlocale(LC_ALL,"");
	//double temp = 0 - ang.yaw*57.30;
        double temp = 0 ;
	if(temp<0)
		temp+=360;
	double diff = gpsdeg;//odom角度与gps角度的差值，odom单位是弧度，要转换为角度
	// printf("ang.yaw %f diff %f\n",temp,diff);
	ROS_INFO("距离下一个点的距离 %f 角度误差 %f",gpsdis, gpsdeg);

		
		if(gpsdis<0.0001){
			ROS_INFO("到点");
			vel.angular.z = 0;
			vel.linear.x = 0;
			vel_pub.publish(vel);
			return 0;//距离小于1，到达目的地

		}else{
		// 	vel.linear.x = 0.2;
		// 	vel_pub.publish(vel);
		// 	ROS_INFO("未到达目标, 前进");;
		// }

		// if(diff>0&&diff<5 || diff>-5&&diff<0){
		// 	printf("go on\n");;			
		// 	//continue;
		// }else{			
			vel.angular.z = diff*KP/57.3/3;
			ROS_INFO("即将转角 % f    角度误差  %f\n", vel.angular.z, diff);
			//vel.angular.z = 0;
			//if(vel.angular.z > 0.)
			vel.linear.x = 0.3;
			if(diff > 50 || diff <-50){
				ROS_INFO("角度偏差过大，等待转向后再前进");
				vel.linear.x = 0.0;
				vel.angular.z = 0.3;
			}

			vel_pub.publish(vel);
			// printf("change degree\n");
		// }	
		}
	//两个角度的差值乘以比例系数KP就是角速度
	return 0;
}

//gps回调函数
void gpsCallback(const mygps::myGPS& gps)
{
	setlocale(LC_ALL,"");
	ROS_INFO("进入gpsCallback---");
	gps_d = gps.dis;	//gps距离,float64，单位是角度
	ROS_INFO("目标角度 %d，当前的偏航角 %d ", gps.deg  , gps.compass);
	gps_t = 1.0*gps.deg - 1.0*gps.compass;	//gps角度，unit32
	if (gps_d > 50)
		return ;
	else if(gps_d < -50)
		return ;
	//标志位 gps.state    unit16

	ROS_INFO("gps状态 %d \n", gps.state);
	pid(Eul,-gps_t,gps_d);

}

//odom回调函数
// void odomCallback(const nav_msgs::Odometry::ConstPtr & msgs)
// {
// 	odom_quat = msgs.pose.pose.oriention;	//四元数
// 	odom_quat = msgs.get();
// 	//把四元数转为欧拉角
// 	Eul = ToEulerAngles(odom_quat);
// }
// void odomCallback(const nav_msgs::Odometry & msgs)
// {
// 	// odom_quat = msgs.pose.pose.position;	//四元数
// 	odom_quat = msgs.pose.pose.orientation;	//四元数
// 	//把四元数转为欧拉角
// 	Eul = ToEulerAngles(odom_quat);
// }
int main(int argc,char ** argv)
{
	setlocale(LC_ALL,"");
	ros::init(argc,argv,"ctrl");
	ros::NodeHandle n;

	gps_sub = n.subscribe("/deg_dis",10,gpsCallback);	//订阅gps话题
	// printf("erertter\n");
	std::cout<<"tt1";
	// odom_sub = n.subscribe("/odom",10,odomCallback);	//订阅odom话题
	printf("tt1\n");
	vel_pub = n.advertise<geometry_msgs::Twist>("/cmd_vel",10);			//发布速度话题
	printf("tt2\n");
	printf("main gps_d%f  \n", gps_d);
	//调用
	//pid(Eul,gps_t,gps_d);
	//usleep(200);
	printf("tt3\n");
	printf("end main \n");

	ros::spin();

	return 0;
}
//当执行完一组GPS数据(即从起始点到达目标点)后，发布信号（条件变量）给gps端，继续发布点。
