# ffmpeg使用记录

## ubuntn18安装ffmpeg4

- 安装参考 https://ubuntuhandbook.org/index.php/2021/05/install-ffmpeg-4-4-ppa-ubuntu-20-04-21-04/

- 指令参考1： https://self-contained.github.io/FFmpeg/FFmpeg.html
- 指令参考2：https://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion


## 相关操作

- 转码

```shell
ffmpeg -i video.flv video.mp4
```
其中，在 -i 后指定输入文件的文件名，在所有命令的最后指定输出文件的文件名。 如果文件名带有空格，请用双引号将文件名包裹。 上述的 video.mp4 在 -i 参数之后，称为 输出参数 ；反之，在 -i 之前的称为 输入参数

- 截取视频

以想要截取 video.mp4 视频的第2到第5分钟为例。

对于容易计算片段秒数的截取任务（本例中片段长为 (5-2)*60=180秒），可以使用 -t 参数，即指定片段长度：
```shell
ffmpeg -ss 00:02:00 -i video.mp4 -t 180 cut.mp4
```

其中， -ss 参数指定了起始的时间戳记，而 -t 参数指定了片段长度（秒）。

更常见的，不用 -t 指定片段长度，而是用 -to 指定终止时刻：

```shell
ffmpeg -ss 00:02:00 -i video.mp4 -to 00:05:00 -copyts cut.mp4
```

此处的 -copyts 表示沿用原视频的时间轴。这是因为 -i 会重置时间轴；如果不使用 -copyts ，将会使传递给 -ss 的 00:02:00 被重置为视频开始（第0秒），进而导致 -to 00:05:00 会被错误地指定为原视频的第7秒处。

- 将多张图片合成gif

```shell
ffmpeg -r 8 -i out_%d.jpg outc.gif
```

 -r 8 设置帧率为8帧
 
 %d为通配符，我需要合成的图片有8张
