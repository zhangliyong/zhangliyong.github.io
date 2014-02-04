Title: Linux Sysadmin Tools
Date: 2014-02-04
Tags: Linux, sysadmin, bash

下面列出一些自己常用的系统管理的工具，总结一下。

htop
====
[htop](http://hisham.hm/htop/index.php) 是一个替代top的工具，显示信息很详细，功能丰富，一但上手操作也很简单，
[thegeekstuff](http://www.thegeekstuff.com/2011/09/linux-htop-examples/)上有
一篇文章专门介绍了这一工具，正如这篇文章上说的：你一但开始即用htop，就不再回到top了。

![htop](http://hisham.hm/htop/htop-1.0-screenshot.png)

iftop
=====
[iftop](http://www.ex-parrot.com/pdw/iftop/) 实时显示网卡的带宽使用情况。

![iftop](http://www.ex-parrot.com/pdw/iftop/iftop_normal.png)

![iftop](http://www.ex-parrot.com/pdw/iftop/iftop_ports.png)

iotop
=====
[iotop](http://guichaz.free.fr/iotop/) 是用python编写的显示磁盘IO使用的应用，vmstat可以显示磁盘的整体使用情况，iotop 可以显示各个应用的磁盘使用。

![iotop](http://guichaz.free.fr/iotop/iotop_big.png)
