# The Missing Semester of Your CS Education

B站视频链接：https://www.bilibili.com/video/BV1x7411H7wa

## 1、Shell

命令行提示符(shell prompt)

![image-20220419144555047](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220419_1650350756.png)

`pwd` (present working directory)

![image-20220419145609561](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220419_1650351369.png)

`cd` (change directory)

`.` 当前目录

`..` 上一层目录

`~` 用户目录

`-` 上一次的所在目录

`r`、`w`、`x`

`cp`、`mv`、`rm`、`rmdir`、`mkdir`

`man`(manual pages)

`Ctrl l`=`clear`

`stream`流

重定向流的方法：(默认的输出流是当前的终端)

`<` 重定向输入流

`>` 重定向输出流(复写 overwrite)

`cat`

`>>` 追加 append

`|`  管道 pipe：取程左边程序的输出作为右边程序的输入

`tail` 打印文件的最后几行 `tail [Option]... [File]...`

`sudo`

`xdg-open File` 选择一个合适的软件打开文件 

### shell变量

普通变量

字符串变量：

​	在字符串前后添加双引号`"`：可以解析字符串中的变量

​	在字符串前后添加双引号`'`：无法解析字符串中的变量

source 脚本，脚本中的函数会被加载到当前终端的环境中

脚本中的`$0`表示脚本的名称

`$?` 返回是一条命令的错误值，当命令正常执行时，返回值是`0`

`$_` 返回上条命令的最后一个参数

`!!` 返回上一条指令

`;` 连接中断中同一行的命令

`变量名=$(命令)` 将命令的结果存放到变量中

在脚本中，`$#` 的值是脚本参数的个数，`$$` 的值是本次脚本运行的`PID`，`$@` 展开所有的参数

![image-20220420224048555](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220420_1650465648.png)

![image-20220420224058832](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220420_1650465658.png)

通配符 `?` ，代替任何一个字符，通配符`*`，代替多个任意字符，`**`匹配零或多个目录名

`{ }` 内容展开

![无标题](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220421_1650510438.png)

检查shell脚本语法是否准确——shellcheck

`tldr` 列出命令的简要示例 https://github.com/tldr-pages/tldr

`locate`  查找文件系统中具有指定子串的路径，`updatedb` 更新`located`的索引库，一般系统会定时更新

通过`grep` 查找文件内的指定内容：`grep -R "string" path`，`-R`递归`path`路径，`"string"`要查找的内容

类似功能的命令：`rg` 、`ripgrep` 

`history` 	结合`grep`；

`fzf` 模糊搜索指令

`tree`，`broot`(`tree`的升级版)，`nnn`(交互式的`tree`)

