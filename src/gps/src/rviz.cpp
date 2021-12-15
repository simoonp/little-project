#include <ros/ros.h>
#include <fstream>	//流操作，读写文件
#include <string>
#include <string.h>
#include <std_msgs/String.h>
#include <fcntl.h>	//打开文件
#include <unistd.h>	//读取文件

#include <visualization_msgs/Marker.h>
#include <visualization_msgs/MarkerArray.h> 
#include <cmath>

#include <mygps/myGPS.h>	
// #include <sensor_msgs/NavSatFix.h>

#include <stdlib.h>
#include <vector>
#include <boost/regex.hpp>
#include <boost/algorithm/string/regex.hpp>

#include <typeinfo>
using namespace std;

// #define D_R 0.017453292519943295;
#define R  6370996.81 //地球半径

const double PI=3.14159265358979323846264338328;

const float zoom = 1.0;

string frame_id = "/my_frame";	
double origin_lon=0, origin_lat=0;	//起点经纬度坐标
int GPS_id = 0;

ros::Publisher GPS_marker_pub;	//实时GPS marker点
visualization_msgs::Marker GPS_marker, GPS_text_marker, GPS_direction_marker, GPS_pose_marker;

ros::Subscriber gps_sub;	//订阅gps话题
mygps::myGPS gps_info,gps_info_old;
double get_degree(double lon2,double lat2,double lon1,double lat1);
double get_distance(double lon1,double lat1,double lon2,double lat2);

void gpsCallback(const mygps::myGPS& gps)
{
	setlocale(LC_ALL,"");
	// ROS_INFO("进入gpsCallback---");

	gps_info_old = gps_info;	//更新数据
	gps_info = gps;
	GPS_id++;

	GPS_marker.id = GPS_id;
	if(GPS_id < 2)
		return;
	double lon, lat;	//存储经纬度数据	
	//更新GPS_marker坐标
	GPS_marker.header.stamp = ros::Time::now();
	GPS_marker.action = visualization_msgs::Marker::ADD;
	lon=gps_info.WGS84_lon;
	lat=gps_info.WGS84_lat;
	ROS_INFO("目标点的经纬度是： %lf , %lf", lon, lat);
	ROS_INFO("当前点距离原点：%lf",get_distance(lon, lat, origin_lon, origin_lat));
	double x = zoom*get_distance(lon, lat, origin_lon, origin_lat)*cos(get_degree(lon, lat, origin_lon, origin_lat));
	double y = zoom*get_distance(lon, lat, origin_lon, origin_lat)*sin(get_degree(lon, lat, origin_lon, origin_lat));
	GPS_marker.pose.position.x = x;
	GPS_marker.pose.position.y = y;
	GPS_marker.pose.position.z = 0.4;
	GPS_marker.color.a = 1.0;
	GPS_marker_pub.publish(GPS_marker);

	ROS_INFO("两从测量距离%lf", get_distance(lon, lat, gps_info_old.WGS84_lon,gps_info_old.WGS84_lat));
	//为当前GPS_marker添加序号标记
	// GPS_text_marker.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
	GPS_text_marker.header.stamp = ros::Time::now();
	GPS_text_marker.id = GPS_id ;
	GPS_text_marker.action = visualization_msgs::Marker::ADD;
	GPS_text_marker.pose.position.x = x;
	GPS_text_marker.pose.position.y = y;
	GPS_text_marker.pose.position.z = GPS_marker.pose.position.z + GPS_marker.scale.z;
	ostringstream str;
	str << GPS_id;
	GPS_text_marker.text = str.str();
	GPS_marker_pub.publish(GPS_text_marker);

	//--- 发布前进的方向箭头 start ----
	float len ;
	len = gps_info.dis * zoom;
	geometry_msgs::Point start_p, end_p;
	GPS_direction_marker.header.stamp = ros::Time::now();
	GPS_direction_marker.id = GPS_id;
	GPS_direction_marker.action = visualization_msgs::Marker::ADD;
	GPS_direction_marker.color.a = 1.0;
	GPS_direction_marker.points.clear();
	start_p.x = GPS_marker.pose.position.x;
	start_p.y = GPS_marker.pose.position.y;
	start_p.z = GPS_marker.pose.position.z;
	GPS_direction_marker.points.push_back(start_p);
	end_p.x = start_p.x + len*cos(gps_info.deg/180.0*PI);
	end_p.y = start_p.y + len*sin(gps_info.deg/180.0*PI);
	end_p.z = start_p.z;
	GPS_direction_marker.points.push_back(end_p);
	GPS_direction_marker.lifetime = ros::Duration();
	GPS_marker_pub.publish(GPS_direction_marker);
	//---发布前进的方向箭头 end ---

	//---发布IMU朝向的方向箭头 start ---
	GPS_pose_marker.header.stamp = ros::Time::now();
	GPS_pose_marker.id = 0;
	GPS_pose_marker.action = visualization_msgs::Marker::ADD;
	GPS_pose_marker.points.clear();
	len = 10*zoom;
	start_p.x = GPS_marker.pose.position.x;
	start_p.y = GPS_marker.pose.position.y;
	start_p.z = GPS_marker.pose.position.z;
	GPS_pose_marker.points.push_back(start_p);
	printf("IMU的值 ：%d\n",gps_info.compass);
	end_p.x = start_p.x +  len *cos(gps_info.compass/180.0*PI);
	end_p.y = start_p.y +  len *sin(gps_info.compass/180.0*PI);
	end_p.z = start_p.z;
	GPS_pose_marker.points.push_back(end_p);
	GPS_pose_marker.lifetime = ros::Duration();
	GPS_marker_pub.publish(GPS_pose_marker);
	//---发布IMU朝向的方向箭头 end ---

	//-----------------------
	//---将上一个位置的Marker变成半透明----start---
	lon=gps_info_old.WGS84_lon;
	lat=gps_info_old.WGS84_lat;
	x = zoom*get_distance(lon, lat, origin_lon, origin_lat)*cos(get_degree(lon, lat, origin_lon, origin_lat));
	y = zoom*get_distance(lon, lat, origin_lon, origin_lat)*sin(get_degree(lon, lat, origin_lon, origin_lat));

	GPS_marker.header.stamp = ros::Time::now();
	GPS_marker.id = GPS_id - 1;
	GPS_marker.action = visualization_msgs::Marker::ADD;
	GPS_marker.pose.position.x = x;
	GPS_marker.pose.position.y = y;
	GPS_marker.color.a = 0.2;
	GPS_marker_pub.publish(GPS_marker);	
	//---将上一个位置的Marker变成半透明----end---

	//---将上一个箭头变成半透明 --start ---
	len = 6*zoom;
	GPS_direction_marker.header.stamp = ros::Time::now();
	GPS_direction_marker.id = GPS_id - 1;
	GPS_direction_marker.action = visualization_msgs::Marker::ADD;
	GPS_direction_marker.color.a = 0.5;
	GPS_direction_marker.points.clear();

	start_p.x = GPS_marker.pose.position.x;
	start_p.y = GPS_marker.pose.position.y;
	start_p.z = GPS_marker.pose.position.z;
	GPS_direction_marker.points.push_back(start_p);
	end_p.x = start_p.x + len*cos(gps_info_old.deg/180.0*PI);
	end_p.y = start_p.y + len*sin(gps_info_old.deg/180.0*PI);
	end_p.z = start_p.z;
	GPS_direction_marker.points.push_back(end_p);
	GPS_direction_marker.lifetime = ros::Duration();
	GPS_marker_pub.publish(GPS_direction_marker);
	//---将上一个箭头变成半透明 --start ---
	// printf("%d\n",GPS_id);

}


// 目标点经纬度 当前点经纬度
double get_degree(double lon2,double lat2,double lon1,double lat1)	
{
	// 角度转弧度
	lat1=lat1*PI/180;
	lon1=lon1*PI/180;

	lat2=lat2*PI/180;
	lon2=lon2*PI/180;

	double a = sin(lon2-lon1) * cos(lat2);
	double b = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2-lon1);

	double result = atan2(a,b);	//  R_D;

	return -result;
}

double get_distance(double lon1,double lat1,double lon2,double lat2)
// double get_distance(double lon2,double lat2,double lon1,double lat1)
{
	double a_lat = lat1 * PI / 180;
	double a_lng = lon1 * PI / 180;
	double b_lng = lon2 * PI / 180;
	double b_lat = lat2 * PI / 180;

	double distance = R * acos(sin(a_lat) * sin(b_lat) + cos(a_lat) * cos(b_lat) * cos(b_lng - a_lng));
	// printf("距离：%f\n",distance);
	return distance;
}

int main( int argc, char** argv )
{
	setlocale(LC_ALL,"");

	ros::init(argc, argv, "view");  //节点
	ros::NodeHandle n;
	ros::Rate r(1);
	gps_sub = n.subscribe("/deg_dis",10,gpsCallback);	//订阅gps话题

//---Marker相关 start-------------
	//---全局路径Marker相关 start-------------
	ros::Publisher path_point_pub = n.advertise<visualization_msgs::MarkerArray>("path_point",20);	
		// 全局路径标记点
	ros::Publisher path_text_pub = n.advertise<visualization_msgs::MarkerArray>("textArray",20);  //----
		// 全局路径标记点文字提示
	ros::Publisher path_line_strip_pub = n.advertise<visualization_msgs::Marker>("path_line_strip", 10);
		//全局路径折线段
	visualization_msgs::MarkerArray path_point;
	visualization_msgs::MarkerArray path_text;
	visualization_msgs::Marker path_line_strip;	
	//---全局路径Marker相关 end------------

	//---坐标系发布 start--- 红色-x 绿色-y 蓝色-z
	ros::Publisher pose_pub = n.advertise<visualization_msgs::Marker>("pose", 20); //话题名称	
	//---坐标系发布 end--- 红色-x 绿色-y 蓝色-z

	//--- GPS坐标实时发布 start-----
	GPS_marker_pub = n.advertise<visualization_msgs::Marker>("GPS_marker", 10);
	// ros::spin();
		//---GPS_marker初始化---start---
	GPS_marker.type = visualization_msgs::Marker::SPHERE;
	GPS_marker.header.frame_id = frame_id;
	GPS_marker.ns = "GPS_space";
	GPS_marker.scale.x = 0.5 *zoom;
	GPS_marker.scale.y = 0.5 *zoom;
	GPS_marker.scale.z = 0.5 *zoom;
	GPS_marker.color.r = 255/255.0;
	GPS_marker.color.g = 165/255.0;
	GPS_marker.color.b = 0/255.0;
	GPS_marker.color.a = 1.0;
	GPS_marker.lifetime = ros::Duration();
	GPS_marker.pose.orientation.x = 0.0;
	GPS_marker.pose.orientation.y = 0.0;
	GPS_marker.pose.orientation.z = 0.0;
	GPS_marker.pose.orientation.w = 1.0;
		//---GPS_marker初始化---end------	
		//--- GPS_text_marker 初始化--- start ---		
	GPS_text_marker.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
	GPS_text_marker.header.frame_id = frame_id;
	GPS_text_marker.ns = "GPS_text_space";
	GPS_text_marker.pose.orientation.x = 0.0;
	GPS_text_marker.pose.orientation.y = 0.0;
	GPS_text_marker.pose.orientation.z = 0.0;
	GPS_text_marker.pose.orientation.w = 1.0;
	GPS_text_marker.scale.z = 0.1;
	GPS_text_marker.color.r = 1.0;
	GPS_text_marker.color.g = 1.0;
	GPS_text_marker.color.b = 1.0;
	GPS_text_marker.color.a = 1.0;
	GPS_text_marker.lifetime = ros::Duration();
		//--- GPS_text_marker 初始化---	end ---	
		//----GPS_direction_marker 初始化-- start-----
	GPS_direction_marker.type = visualization_msgs::Marker::ARROW;
	GPS_direction_marker.header.frame_id = frame_id;
	GPS_direction_marker.ns = "GPS_direction_space";
	GPS_direction_marker.pose.orientation.w = 1.0;
	GPS_direction_marker.color.r = 192/255.0;
	GPS_direction_marker.color.g = 255/255.0;
	GPS_direction_marker.color.b = 62/255.0;
	GPS_direction_marker.color.a = 1.0;
	GPS_direction_marker.scale.x=0.2 *zoom;
	GPS_direction_marker.scale.y=0.5*zoom;
	GPS_direction_marker.scale.z=2*zoom;
	GPS_direction_marker.lifetime = ros::Duration();
		//----GPS_direction_marker 初始化-- start-----

		//----GPS_pose_marker 初始化-- start-----
	GPS_pose_marker.type = visualization_msgs::Marker::ARROW;
	GPS_pose_marker.header.frame_id = frame_id;
	GPS_pose_marker.ns = "GPS_pose_space";
	GPS_pose_marker.pose.orientation.w = 1.0;
	GPS_pose_marker.color.b = 1.0;
	GPS_pose_marker.color.a = 1.0;
	GPS_pose_marker.scale.x=0.1*zoom;
	GPS_pose_marker.scale.y=0.5*zoom;
	GPS_pose_marker.scale.z=2*zoom;
	GPS_pose_marker.lifetime = ros::Duration();
		//----GPS_pose_marker 初始化-- end-----

	//--- GPS坐标实时发布 end-----

	//-----全局路径折线段 初始化 start ---
	path_line_strip.header.frame_id = frame_id;
	path_line_strip.header.stamp = ros::Time::now();
	path_line_strip.ns = "path_line_space";
	path_line_strip.action = visualization_msgs::Marker::ADD;
	path_line_strip.type = visualization_msgs::Marker::LINE_STRIP;
	path_line_strip.pose.orientation.w = 1.0;
	path_line_strip.id = 1;
	path_line_strip.scale.x = 0.1;	//设置线条粗细
	path_line_strip.color.r = 208/255.0;
	path_line_strip.color.g = 32/255.0;	
	path_line_strip.color.b = 144/255.0;	
	path_line_strip.color.a = 1.0;	
	//-----全局路径折线段 end ---

//----Marker相关 end-------------

//--- 文件读取与参数初始化 start ----
	string file_path;
	// file_path = getenv("HOME") + string("/gps_ws/src/mygps/info/path");	//getenv("HOME") 获取用户目录
	// file_path = getenv("HOME") + string("/gps_ws/src/mygps/info/aaa");	//getenv("HOME") 获取用户目录
	file_path = getenv("HOME") + string("/gps_ws/src/mygps/info/p80");	//getenv("HOME") 获取用户目录


	// file_path = getenv("HOME") + string("/gps_ws/src/mygps/info/gcj02file.txt");	//getenv("HOME") 获取用户目录
	ifstream readfile;

	char data[1000];	//存储文本数据
	string datastr;
	int datalen;	//获取长度，用于剔除时间戳和跳出循环
	double lon, lat;	//存储经纬度数据

	vector <string> lon_lat_list, lon_lat;
	
	int time_i = 0;

	//------获取方位角数据测试--start---------
	/*
	^N
				*
				30
				*
	W <- *****105****106,29****07**** -> E
				* 
				28 
				* 
	*/
	if(1){
		printf("东北方向%f\n",get_degree(107,30,origin_lon,origin_lat)/(PI / 180));
		printf("东南方向%f\n",get_degree(107,28,origin_lon,origin_lat)/(PI / 180));
		printf("西南方向%f\n",get_degree(106,28,origin_lon,origin_lat)/(PI / 180));
		printf("西北方向%f\n",get_degree(106,30,origin_lon,origin_lat)/(PI / 180));
	}
	//------获取方位角数据测试--end----------
	//--- 文件读取与参数初始化 end ----

	//-----------------处理整个高德地图数据的经纬度 start------------------
	
	int load_flag=1;//全局路径加载标志

	int start_id = 3;

	while(ros::ok()){

		// 等待GPS提供起点位置
		if (GPS_id < start_id)
		{
			ROS_INFO("--等待GPS提供起点位置-- %d", GPS_id);
			ros::spinOnce();
			r.sleep();
			continue;
		}
		if (GPS_id == start_id && gps_info.plan_flag){
			origin_lon = gps_info.WGS84_lon;
			origin_lat = gps_info.WGS84_lat;
			ROS_INFO("设置原点完成");
		}

			//----rviz显示坐标系箭头 start ---
		for (int i = 0; i < 3; i++)
		{
			// printf("画箭头\n");
			
			visualization_msgs::Marker pose_marker;
			pose_marker.header.frame_id = frame_id;	

			pose_marker.ns = "pose_space";
			
			pose_marker.type = visualization_msgs::Marker::ARROW;
			pose_marker.action = visualization_msgs::Marker::ADD;
			
			pose_marker.header.stamp = ros::Time::now();
			pose_marker.id = i;
			pose_marker.pose.orientation.w = 1.0;
			// pose_marker.

			geometry_msgs::Point start_p, end_p;
			start_p.x = 0;
			start_p.y = 0;
			start_p.z = 0;
			pose_marker.points.push_back(start_p);	
			
			end_p.x = 0;
			end_p.y = 0;
			end_p.z = 0;
			if (i==0){
				end_p.x = zoom * 5;
				pose_marker.color.r=1.0;
				// printf("-\n");
			}else if(i==1){
				end_p.y = zoom * 5;
				pose_marker.color.g=1.0;
				// printf("--\n");		
			}else if(i==2){
				end_p.z = zoom * 5;
				pose_marker.color.b=1.0;
				// printf("---\n");
			}
			pose_marker.color.a=1.0;
			pose_marker.points.push_back(end_p);

			pose_marker.scale.x=1 * zoom;
			pose_marker.scale.y=2 * zoom;
			pose_marker.scale.z=1 * zoom;

			pose_marker.lifetime = ros::Duration();
			pose_pub.publish(pose_marker);
		}
			//----rviz显示坐标系箭头 end ---


		if(load_flag == 1)
		{
			readfile.open(file_path.c_str());	//读取文件
			if(readfile.bad()){
				ROS_INFO("读取文件失败");
				return -1;
			}else{
				printf("正在运行\n");
				// while (!readfile.eof())	//判断文件是否到结尾
			}
			int marker_id=0;	

			int tmp_i = 0;
			int tmp_j = 0;
			while (!readfile.eof())	//判断文件是否到结尾
			{
				readfile >> data;
				tmp_i++;
				// if(tmp_i%37 == 0){
				if(1){
					
				tmp_j++;
				cout << "这是 j " << tmp_j << endl;
				printf("%d \n", tmp_i);
				printf("读取新一行\n");
				// readfile >> data;

				cout << "--data: " << data << endl;


				datastr=string(data);	//字符数组转换为字符串
				if(data[0]=='-' && data[1]=='-')
					break;
					

				boost::split_regex(lon_lat,datastr,boost::regex(","));	

	
				lon = stod(lon_lat[0].c_str());
				lat = stod(lon_lat[1].c_str());
				
				// 数据处理结束 end------------------------
				printf("分割字符串 lon : %f lat :%f \n 原点：%f %f \n", lon, lat, origin_lon, origin_lat);
				double x = get_distance(lon, lat, origin_lon, origin_lat)*cos(get_degree(lon, lat, origin_lon, origin_lat));
				double y = get_distance(lon, lat, origin_lon, origin_lat)*sin(get_degree(lon, lat, origin_lon, origin_lat));
				printf("%f, %f \n",x, y);

				//---Marker相关 start-------------

				//---全局路径Marker相关 start-------------
				visualization_msgs::Marker path_marker;
				path_marker.header.frame_id = frame_id;
				path_marker.header.stamp = ros::Time::now();

				path_marker.ns = "path_space";
				marker_id++;
				path_marker.id = marker_id;
				// printf("----%d-----\n",path_marker.id);
				path_marker.type = visualization_msgs::Marker::SPHERE;
				path_marker.action = visualization_msgs::Marker::ADD;
				

				path_marker.pose.position.x = x * zoom;
				path_marker.pose.position.y = y * zoom;
				path_marker.pose.position.z = 0;
				path_marker.pose.orientation.x = 0.0;
				path_marker.pose.orientation.y = 0.0;
				path_marker.pose.orientation.z = 0.0;
				path_marker.pose.orientation.w = 1.0;

				path_marker.scale.x = 0.3;
				path_marker.scale.y = 0.3;
				path_marker.scale.z = 0.30;

				path_marker.color.r = 0.0f;
				path_marker.color.g = 1.0f;
				path_marker.color.b = 0.0f;
				path_marker.color.a = 1.0;

				path_marker.lifetime = ros::Duration();
				if(load_flag == 1)
					path_point.markers.push_back(path_marker);	
					//同一个id的Marker重复push会报错“Adding marker 'path_space/1' multiple times. ”
					// 多次添加标记“path_space/1”。

				// path_point_pub.publish(path_point);
					//---全局路径Marker相关 end-------------

					//---Marker文本显示 start-------------
				visualization_msgs::Marker path_text_marker;
				path_text_marker.header.frame_id = frame_id;
				path_text_marker.header.stamp = path_marker.header.stamp;

				path_text_marker.ns = "text_space";
				path_text_marker.id = marker_id;

				path_text_marker.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
				path_text_marker.action = visualization_msgs::Marker::ADD;

				path_text_marker.pose.position.x = path_marker.pose.position.x;
				path_text_marker.pose.position.y = path_marker.pose.position.y;
				path_text_marker.pose.position.z = path_marker.scale.z;
				path_text_marker.pose.orientation.x = 0.0;
				path_text_marker.pose.orientation.y = 0.0;
				path_text_marker.pose.orientation.z = 0.0;
				path_text_marker.pose.orientation.w = 1.0;					
				
				path_text_marker.scale.z = 0.30;	//控制字体大小
				
				path_text_marker.color.r = 0.0f;
				path_text_marker.color.g = 1.0f;
				path_text_marker.color.b = 1.0f;
				path_text_marker.color.a = 1.0;

				ostringstream str;
				str << marker_id;	//写入文本内容
				path_text_marker.text=str.str();

				path_text_marker.lifetime = ros::Duration();
				if(load_flag == 1)				
							path_text.markers.push_back(path_text_marker);
				//---Marker文本显示 end-------------

				//-----全局路径折线段 start ---
				geometry_msgs::Point p;
				p.x = path_marker.pose.position.x;
				p.y = path_marker.pose.position.y;
				p.z = path_marker.pose.position.z;
				
				path_line_strip.points.push_back(p);
				//-----全局路径折线段 end ---
				//---Marker相关 end-------------
			}
			}
			// path_text_pub.publish(path_text);
			// path_point_pub.publish(path_point);
			// path_line_strip_pub.publish(path_line_strip);
			printf("文本读取完毕\n");

		load_flag++; //加载完成
		readfile.close();
		// 	break;
		
	}
		path_text_pub.publish(path_text);
		path_point_pub.publish(path_point);
		path_line_strip_pub.publish(path_line_strip);
		//------------------------------------
		ros::spinOnce();
		r.sleep();
	}
	// ros::spin();
	return 0;
}
