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

all=$((p1+p2+p3))
echo "-------------------"
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
echo "总功率为 $all mV"
#echo "总功率为 $((p1+p2+p3)) mV"

echo $all >> power.log
