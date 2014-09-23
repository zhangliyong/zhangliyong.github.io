Title: Mongodb NUMA 导致的性能问题
Tags: MongoDB, DB

最近升级了mongodb，用mongo连接mongod后出现如下warning:

    Server has startup warnings:
    Mon Oct 29 14:45:23 [initandlisten]
    Mon Oct 29 14:45:23 [initandlisten] ** WARNING: You are running on a NUMA machine.
    Mon Oct 29 14:45:23 [initandlisten] **          We suggest launching mongod like this to avoid performance problems:
    Mon Oct 29 14:45:23 [initandlisten] **              numactl --interleave=all mongod [other options]

随即查了下*NUMA*是什么，有多篇文章均提到了NUMA会导致mongodb的性能问题，而且官方文档也有说明。

>To disable NUMA for MongoDB, use the numactl command and start mongod in the following manner:

     numactl --interleave=all /usr/bin/local/mongod

>Adjust the proc settings using the following command:

    echo 0 > /proc/sys/vm/zone_reclaim_mode
>To fully disable NUMA you must perform both operations. However, you can change zone_reclaim_mode without restarting mongod. For more information, see documentation on Proc/sys/vm.

在此做一个整理：

NUMA：NUMA是多核心CPU架构中的一种，其全称为Non-Uniform Memory Access，简单来说就是在多核心CPU中，机器的物理内存是分配给各个核的，架构简图如下所示：

![NUMA](http://jcole.us/blog/files/numa-architecture.png)

每个核访问分配给自己的内存会比访问分配给其它核的内存要快，有下面几种访问控制策略：

1. 缺省(default)：总是在本地节点分配（分配在当前进程运行的节点上）；
2. 绑定(bind)：强制分配到指定节点上；
3. 交叉(interleave)：在所有节点或者指定的节点上交织分配；
4. 优先(preferred)：在指定节点上分配，失败则在其他节点上分配。

上面文章中最后使用numactl –interleave命令就是指定其为交叉共享模式。

我们知道虚拟内存机制是通过一个中断信号来通知虚拟内存系统进行内存swap的，所以这个irqbalance进程忙，是一个危险信号，在这里是由于在进行频繁的内存交换。这种频繁交换现象称为swap insanity，在MySQL中经常提到，也就是在NUMA框架中，采用不合适的策略，导致核心只能从指定内存块节点上分配内存，即使总内存还有富余，也会由于当前节点内存不足时产生大量的swap操作。


### Install

在Ubuntu下以numactl的命令启动mongodb，要先安装numactl

    sudo apt-get install numactl

###参考：

http://docs.mongodb.org/manual/administration/production-notes/#production-numa

http://huoding.com/2011/08/09/104

http://blog.jcole.us/2010/09/28/mysql-swap-insanity-and-the-numa-architecture/

http://blog.nosqlfan.com/html/2772.html
