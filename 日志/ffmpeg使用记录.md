# ffmpeg使用记录

## ubuntn18安装ffmpeg4

- 安装参考 https://ubuntuhandbook.org/index.php/2021/05/install-ffmpeg-4-4-ppa-ubuntu-20-04-21-04/

- 指令参考1： https://self-contained.github.io/FFmpeg/FFmpeg.html
- 指令参考2：https://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion


## 相关操作

- 查看视频属性

```shell
ffmpeg -i video.mp4
```
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

*使用的这条指令的时候遇到个小问题，以该条指令为例，输出的视频，内容只有3min，但是这个视频长度有5min，后面2min是空白，使用 ffmpeg -i video.mp4 -ss 00:02:00 -to 00:05:00 -copyts cut.mp4 可以的到想要的结果*
- 将多张图片合成gif

```shell
ffmpeg -r 8 -i out_%d.jpg outc.gif
```

 -r 8 设置帧率为8帧

 %d为通配符，我需要合成的图片有8张

 - 提取音频

```shell
$ ffmpeg -i video.mp4 -c:a copy audio.aac
```
此处的 -c:a 表示音频流；视频流 -c:v 与字幕流 -c:s 自然也类似。 注意：如果音频流与容器冲突时，你需要将 copy 改为正确的编解码器（或者删去 -c:a copy 来让 FFmpeg 自动选择），以执行重编码。

- 合并音频和视频

```shell
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -strict experimental output.mp4
```

- 去除音频，只保留视频

