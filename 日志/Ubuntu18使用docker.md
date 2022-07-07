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
# -i 保证容器的STDIN时开启的，
# -t 告诉Docker创建一个伪tty终端
# -d, --detach=false 指定容器运行于前台还是后台，默认为false
# --name参数将Ubuntu容器重命名为ubuntu-test

# 通过 exec 命令进入 ubuntu 容器
$ docker exec -it ubuntu-test /bin/bash
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/ubuntu_test.png)

run的其他参数

    Usage: docker run [OPTIONS] IMAGE [COMMAND] [ARG...]    
    -d, --detach=false         指定容器运行于前台还是后台，默认为false     
    -i, --interactive=false   打开STDIN，用于控制台交互    
    -t, --tty=false            分配tty设备，该可以支持终端登录，默认为false    
    -u, --user=""              指定容器的用户    
    -a, --attach=[]            登录容器（必须是以docker run -d启动的容器）  
    -w, --workdir=""           指定容器的工作目录   
    -c, --cpu-shares=0        设置容器CPU权重，在CPU共享场景使用    
    -e, --env=[]               指定环境变量，容器中可以使用该环境变量    
    -m, --memory=""            指定容器的内存上限    
    -P, --publish-all=false    指定容器暴露的端口    
    -p, --publish=[]           指定容器暴露的端口   
    -h, --hostname=""          指定容器的主机名    
    -v, --volume=[]            给容器挂载存储卷，挂载到容器的某个目录    
    --volumes-from=[]          给容器挂载其他容器上的卷，挂载到容器的某个目录  
    --cap-add=[]               添加权限，权限清单详见：http://linux.die.net/man/7/capabilities    
    --cap-drop=[]              删除权限，权限清单详见：http://linux.die.net/man/7/capabilities    
    --cidfile=""               运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法    
    --cpuset=""                设置容器可以使用哪些CPU，此参数可以用来容器独占CPU    
    --device=[]                添加主机设备给容器，相当于设备直通    
    --dns=[]                   指定容器的dns服务器    
    --dns-search=[]            指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件    
    --entrypoint=""            覆盖image的入口点    
    --env-file=[]              指定环境变量文件，文件格式为每行一个环境变量    
    --expose=[]                指定容器暴露的端口，即修改镜像的暴露端口    
    --link=[]                  指定容器间的关联，使用其他容器的IP、env等信息    
    --lxc-conf=[]              指定容器的配置文件，只有在指定--exec-driver=lxc时使用    
    --name=""                  指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字    
    --net="bridge"             容器网络设置:  
                                  bridge 使用docker daemon指定的网桥       
                                  host    //容器使用主机的网络    
                                  container:NAME_or_ID  >//使用其他容器的网路，共享IP和PORT等网络资源    
                                  none 容器使用自己的网络（类似--net=bridge），但是不进行配置   
    --privileged=false         指定容器是否为特权容器，特权容器拥有所有的capabilities    
    --restart="no"             指定容器停止后的重启策略:  
                                  no：容器退出时不重启    
                                  on-failure：容器故障退出（返回值非零）时重启   
                                  always：容器退出时总是重启    
    --rm=false                 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)    
    --sig-proxy=true           设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理    

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

- 使用 apt-get update 更新软件，安装vim

```shell
# 如果还未进入容器，用exec命令进入容器
$ docker exec -it ubuntu-test /bin/bash

root@9508ab4a4a0e:~# apt-get update

root@9508ab4a4a0e:~# apt-get install vim
```
*容器里 apt 好像无法使用，只能用apt-get*

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/update.png)

可以用 docker ps -a 指令查看所有容器（包含已停止运行的容器）

```shell
dingfang@dingfang-Inspiron-5457:~$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED        STATUS                    PORTS     NAMES
eeeaeb265831   ubuntu        "/bin/echo 'Hello wo…"   40 hours ago   Exited (0) 40 hours ago             reverent_elion
9508ab4a4a0e   ubuntu        "bash"                   40 hours ago   Up 40 hours                         ubuntu-test
2a6ea3ac122c   hello-world   "/hello"                 41 hours ago   Exited (0) 41 hours ago             distracted_hugle
9a2ff756cdb6   hello-world   "/hello"                 41 hours ago   Exited (0) 41 hours ago             cool_noether
595ef3df6f20   hello-world   "/hello"                 41 hours ago   Exited (0) 41 hours ago             trusting_mcnulty
```
*短UUID(如 9508ab4a4a0e)和 名称(如 ubuntu-test)都可以唯一指定容器*

- 通过 start 重新启动停止的容器

```shell
# docker start UUID/名称
$ docker start ubuntu-test

# 使用 attach 命令进入正在运行的容器
$ docker attach ubuntu-test
# 若容器未运行，提示报错：You cannot attach to a stopped container, start it first
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/docker/start.png)

```shell
# 查看容器最新的几条日志
$ docker logs  ubuntu-test

# 监视容器最新的几条日志
$ docker logs -f ubuntu-test

# 查看容器的进程
$ docker top ubuntu-test

# 查看容器的统计信息
$ docker start ubuntu-test
```

- 在容器内运行进程

通过 docker exec 命令可以在容器内部运行额外的新进程
```shell
$ docker exec -d 容器名 需要执行的命令
# -d 开启一个后台进程，-it 开启交互式进程
```

- 停止守护式容器

```shell
$ docker stop UUID/容器名称
```