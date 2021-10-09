# Ubuntu 18 安装 docker

## 手动安装
- 卸载原先的Docker

```shell
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```

由于是第一次装，所以啥也没卸载成

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/uninstall.png)

- 更新软件源，安装相关工具

```shell
$ sudo apt update
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
```

- 添加Docker官方的GPG密钥

```shell
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

```

- 设置稳定版仓库

```shell
$ sudo add-apt-repository "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/ $(lsb_release -cs) stable"
```

*注：lsb_release -cs 指令可以查看Ubuntu的版本*

- 安装 Docker Engine-Community

```shell
# 更新 apt 包索引
$ sudo apt-get update

# 安装最新版本的 Docker Engine-Community 和 containerd
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

也可以安装特定版本

```shell
# 查看仓库中可用的版本
$ apt-cache madison docker-ce

# 使用第二列中的版本字符串安装特定版本，如下图所示，例如 5:20.10.9~3-0~ubuntu-bionic
# 用第二列的版本号代替<VERSION_STRING>
$ sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
```
![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/madison.png)

- 测试 Docker 是否安装成功

```shell
$ sudo docker run hello-world
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/docker_hello.png)

- 非 root 用户使用Docker

```shell
# 创建docker组
$ sudo groupadd docker

#将用户加到docker组中
$ sudo usermod -aG docker $USER
#注销账户重新登录，之后运行docker就不用加sudo了
```
![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/groupadd_docker.png)

*注：安装Docker后，系统好像会自动创建docker组*
## 删除Docker

```shell
# 删除安装包：
$  sudo apt-get purge docker-ce docker-ce-cli containerd.io

# 删除镜像、容器、配置文件等内容：
$ sudo rm -rf /var/lib/docker
$ sudo rm -rf /var/lib/containerd
# 主机上的镜像、容器、卷或自定义配置文件不会自动删除
```

# Docker使用

## Docker Hello World

- Docker安装Ubuntu

访问Ubuntu镜像库地址：https://hub.docker.com/_/ubuntu?tab=tags&page=1&ordering=last_updated

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/ubuntu.png)

```shell
# 拉取最新版的 Ubuntu 镜像
$ docker pull ubuntu
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/pull_ubuntu.png)

```shell
# 查看本地镜像
$ docker images
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/docker_image.png)

*注：hello-world是刚刚的 docker run hello-world 命令产生的*
```shell
# 4、运行容器，并且可以通过 exec 命令进入 ubuntu 容器
$ docker run -itd --name ubuntu-test ubuntu
# --name参数将Ubuntu容器重命名为ubuntu-test

# 通过 exec 命令进入 ubuntu 容器
$ docker exec -it ubuntu-test /bin/bash
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/ubuntu_test.png)

```shell
# 通过 docker ps 命令查看容器的运行信息：
$ docker ps
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/docker_ps.png)

- 在容器里运行 hello world

```shell
$ docker run ubuntu /bin/echo "Hello world"
```
    docker: Docker 的二进制执行文件。

    run: 与前面的 docker 组合来运行一个容器。

    ubuntu 指定要运行的镜像，Docker 首先从本地主机上查找镜像是否存在，如果不存在，Docker 就会从镜像仓库 Docker Hub 下载公共镜像。

    /bin/echo "Hello world": 在启动的容器里执行的命令

