Title: MongoDB Storage Internals
Tags: MongoDB, Fragmentation, Disk, Storage
Date: 2014-02-18 09:12


我们都知道MongoDB通过 `mmap` 的方式将存储在磁盘上的数据文件映射到内存中进行操作，那MongoDB是如何组织数据文件的，最近在网上找了相关资源，在此做一个 ** 翻译和汇总 ** , 非原创，原文在下面的参考链接部分。

我们按照从总体到内部的顺序进行分析，

## Data Files
所有的 data files 存储在 `dbpath` 参考所指定的目录中，对应于每个数据库都有一个 、namespace file, 多个journal file 和 data file。

    $ ls -lh /data/db
    drwxr-xr-x 2 mongodb nogroup 4.0K Feb 14 13:14 journal
    -rwxr-xr-x 1 mongodb nogroup    6 Feb 13 16:49 mongod.lock
    -rw------- 1 mongodb nogroup  64M Feb 14 13:15 test.0
    -rw------- 1 mongodb nogroup 128M Feb 14 13:14 test.1
    -rw------- 1 mongodb nogroup  16M Feb 14 13:15 test.ns
    drwxr-xr-x 2 mongodb nogroup 4.0K Feb 14 13:15 _tmp

`mongod.lock` 是MongoDB的lock 文件，可用来判断上次MongoDB是否正常shutdown。

其余的所有文件为 test 数据库的文件。

MongoDB 采用 aggressive pre-allocation的方式申请 data files，而且总会多申请一个备用的data file，如上面的test.1为备用的data file。数据文件会以指数级增长，最大为2GB。

namespace file 内存储了所有的 collection以及index。

data file 存储了所有的document及index。data file 以 extent为逻辑存储单元，每个data file包含多个extents.

## Extents
每个extent被用来存储doucments或者index。

extents与data file之间的关系

![extents and data file](http://blog.mongolab.com/wp-content/uploads/2014/01/data_extents1.png)

extents与namespace file之间的关系

![extents and namespace file](https://www.evernote.com/shard/s30/sh/7fd6636c-36b9-40a9-b83e-593e248ad8df/d8138c78d9127af7b2edb153d68ed02c/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

**NOTE**:

* 一个extent只能存储一个collection的documents或index，不能同时用来存储documents和index。
* 一个collection通常会有多个extents。
* 当需要一个新的extent时会在当前data file中申请extent，如果当前data file空间不足，则申请新的data file.

同一个collection的所有extents通过指针连接，namespace file中的collection只需要指向其第一个extent即可。

![extents](https://www.evernote.com/shard/s30/sh/948ed357-1c61-4d54-bfc3-29694ffaa6ff/0cfd37262cfe8f33dc49cfcf1e9ba242/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

每个extent会存储一些metadata，其余空间存储records。

## Records
每一个record会存储一些metadata及一个document。

![records](https://www.evernote.com/shard/s30/sh/14d51a20-e929-4e6a-95c6-df0929da3f87/0f543bfa0139eb4b503e32c98d0474e7/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

![record allocation](https://www.evernote.com/shard/s30/sh/cc9c8241-32fb-4a88-b794-4bd9430c5887/181d7befe5ea6be0af90f11f235005ed/deep/0/Inside-MongoDB--the-Internals-of-an-Open-Source-Database.png)

## Indexes

MongoDB的索引是BTree结构，序列化到磁盘进行存储，存储在自己的extents中，而且每一个index有一个单独的namespace，并不属于其collection的namespace.

    > db.system.namespaces.find()
    { "name" : "test.system.indexes" }
    { "name" : "test.foo.$_id_" }
    { "name" : "test.foo" }

## Metrics from db.stats()

现在我们知道了MongoDB的数据组织方式，下面分析一下 `db.stats()` 的输出指标所代表的含义。

### dataSize

![data size](http://blog.mongolab.com/wp-content/uploads/2014/01/data_size.png)

dataSize 是所有 documents 的大小总和，包括这个document的padding，也是所有records的总和, 当document被删除时dataSize会变小，但当减小document大小时，dataSize不会变化。

### storageSize

![storageSize](http://blog.mongolab.com/wp-content/uploads/2014/01/storage_size.png)

storageSize是所有extents的大小总和，会比dataSize要大，因为它会包括extents中未被使用的空间，以及因document被删除及移动带来的空闲空间。

当删除或减小document时，storageSize不会变化。

### fileSize

![fileSize](http://blog.mongolab.com/wp-content/uploads/2014/01/file_size.png)

fileSize 包括所有的data extents, index extents以及data file中未使用的空间，是数据库存储在磁盘上的文件大小。会比storageSize要大，因为它还包括index extents，以及未使用的空间。

**NOTE:** dataSize 和 storageSize 都不包括index。

当删除数据库时，fileSize会变化，因为此数据库相应的data file会被删除，但当删除collection，documents及index时fileSize不会变化。

### nsSize

namespace(`test.ns`)文件的大小。namespace file的大小是固定的，但可以通过修改nssize参数调整。


## Fragmentation

当执行 `update` 及 `remove` 操作时会产生fragmentation.

![fragmentation](https://www.evernote.com/shard/s30/sh/7fe5f0f5-0453-422d-b10c-44d7858e8f3a/6c4a17b9b49476734e37440f829ee5f8/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

如果文档的大小不固定，而且经常发生变化，则会产生大量的 fragmentation，这样会浪费内存及磁盘空间，增加Disk IO，而且由于update操作引起的文档移动还会导致索引的更新，使写操作变慢。可以通过比较 `db.collection.stats()` 输出中的 `size` 和 `storageSize` 来判断fragmentation的状况。

### How to Combat

* 定时执行 `compact` ，会lock数据库，要在secondary上执行。
* 设定 collection schema, 使document不会增大
* pre-pad documents, 使document不会增大。
* 使用不同的collection, 尽量使用 `db.collection.drop()` 代替 `db.collection.remove()` 删除数据
* 设置 `usePowerOf2sizes` 提高空间的重用度。

[MongoDB Exorcises File Fragmentation Demons](http://linux.sys-con.com/node/2756958/mobile) 介绍了 `usePowerOf2sizes` 所带来的空间利用率及性能的提升。不同的应用场景其效果也不一样。

##参考

http://www.slideshare.net/mongodb/mongodb-london-2013understanding-mongodb-storage-for-performance-and-data-safety-by-christian-kvalheim-10gen

http://blog.mongolab.com/2014/01/how-big-is-your-mongodb/

http://linux.sys-con.com/node/2756958/mobile
