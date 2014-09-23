Title: MongoDB Journal
Tags: MongoDB
Date: 2014-02-18 16:30

启用journal后，MongoDB的操作先写到journal buffer中，每100ms MongoDB会flush journal buffer到磁盘journal中，此时数据不会丢失，

若MongoDB crash，则最多会丢失100ms的数据。

## Journal Files

mongod启动后，会在 `dbpath` 下新建一个 `journal` 目录，这个目录下存放所有的journal文件，journal 文件是append-only，而且文件名以 `j._` 为前缀，每个journal文件的大小为1GB，当journal超过1GB后，会创建新的journal文件，当MongoDB将journal中的所写操作应用到数据文件后，这些journal文件才会被删除。

journal文件的格式为：

![journal](https://www.evernote.com/shard/s30/sh/1da95a5d-e676-4d26-9526-4c88a0f99c6d/55ab60012797fe9541233b5835db1f18/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

## How Journal Works

**NOTE:** 此部分翻译自： http://www.kchodorow.com/blog/2012/10/04/how-mongodbs-journaling-works/

首先磁盘上存储了 journal files和data files，如下：

![journal files and data files](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/mapfile.png)

当启动mongod后，会将data files映射到shared view，并返回其在内存的虚拟地址。例如：数据文件大小为2,000 bytes，操作系统将其映射到内存地址1,000,000-1,002,000，如果你访问地址1,000,042，那你会得到数据文件中从第42个字节开始的数据。（当然操作系统不会把所有数据都load到内存中，只有当你访问到时，才会放到内存中.）

![shared view](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/to_shared.png)

shared view由文件直接映射，当修改了内存中的数据后，OS会将修改flush到对应的数据文件中。这是在没有journal的情况下mongod的工作方式，mongod会每60s将内存中的修改flush到磁盘。

如果启用了journal，mongod会再做一次映射，将shared view映射到private view，这就是为什么启用journal后虚拟内存的使用量翻倍。

![private view](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/to_private.png)

由于private view是由shared view映射来，所以private view的改动不能直接flush到硬盘。

当mongod进行写操作时，会修改private view。

![write](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/write.png)

然后mongod会将这些改动的描述写到journal file, 在journal file中记录哪些文件的哪些字节被修改。

改动的描述会被追加到journal file之后。

![journalled](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/journalled.png)

这时写操作被持久化，不会丢失。如果mongod crash，虽然改动没记录到data file中，journal还可以replay这部分改动。

接下来journal会replay shared view中的改动。

![toshared](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/toshared.png)

然后mongod再重新将shared view映射到private view中，防止private view中有太多的改动。

![remap](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/remap.png)

最后，shared view中的改动flush后硬盘中。默认情况下mongod会要求OS每60s flush一次。每次flush完后，会将journal中flush过的改动删除。

![flushed](http://www.kchodorow.com/blog/wp-content/uploads/2012/10/flushed.png)

这就是journal的工作原理。感谢Richard，他给的解释是我听过的最好的（今年秋季他还会[在线教授 MongoDB](http://education.10gen.com/courses/10gen/M101/2012_Fall/about)）。

## Cost of a Journal

使用journal后写操作的性能会降低5-30%。

对于写操作非常频繁的系统建议journal files和data files使用不同的物理磁盘，它们都会flush数据到磁盘，若使用同一个会使用Disk IO延时增大，降低性能。

对于以读为主的系统，不会有太多影响。

## 参考
http://www.slideshare.net/mongodb/mongodb-london-2013understanding-mongodb-storage-for-performance-and-data-safety-by-christian-kvalheim-10gen

http://www.kchodorow.com/blog/2012/10/04/how-mongodbs-journaling-works/
