# 存放openwrt (MT7620A架构mipsel_24kc)相关固件

## 开启sftp服务

```shell
opkg update
opkg install vsftpd openssh-sftp-server
/etc/init.d/vsftpd enable
/etc/init.d/vsftpd start
```
