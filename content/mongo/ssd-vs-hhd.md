Title: ssd-vs-hhd
Tags: mongodb, ssd, hhd, disk


随机MongoDB的数据量增大，我们服务器的磁盘利用率不数据增加，一度接近100%，而且
Disk IO成为MongoDB的性能瓶颈，在进行sharding之前，我们决定先迁移到使用SSD的服务
器，下面我利用 `mongoperf` 工具对HHD和SSD的 R/W 进行了一个测评。

结果如下：

[gist:id=8931586]

可以看到HHD的读取速度为6-7MB/s，SSD的为150MB/s左右，为HHD的20多倍。

再看写的速度，HHD最高为6MB/s，SSD最高为39MB/s，为HHD的6倍多。

使用SSD后，可以大大减小Disk IO的延时，提高MongoDB响应速度，
但SSD的价格比较高，如果学着SSD性价比低，可以配置sharding。
