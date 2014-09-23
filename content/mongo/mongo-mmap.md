Title: MongoDB mmap
Tags: MongoDB, mmap, Linux
Date: 2014-02-18 15:12

MongoDB 使用系统调用 `mmap` 将数据文件映射到内存，然后直接操作内存。

这样简化了MongoDB的开发，可以省去复杂的内存及磁盘操作相关的代码，完全不用关心文件系统的类型，OS会自动cache数据，并使用LRU的方式，而且MongoDB重启后可以继续使用cache中的数据。

当然也会有缺点，数据文件碎片(fragmentation)会影响内存的使用，而且操作系统的 `read-ahead` 也会影响内存的使用，对于索引数据来说，cache的LRU方式并不合适，索引数据最好一直在内存中。

MongoDB 进程的虚拟内存 `virtual size = total files size + overhead(connections, heap)`

如果MongoDB启动时启用了journal，则virtual size会翻倍。

![mongodb mmap](https://www.evernote.com/shard/s30/sh/e52f6016-74cb-44f4-b821-b09a4211e4db/6b0227c2023075510f625d5211add1c6/deep/0/MongoDB-London-2013-Understanding-MongoDB-Storage-for-Performance-a....png)

TODO: add mmap fundermentals


## 参考

http://www.slideshare.net/mongodb/mongodb-london-2013understanding-mongodb-storage-for-performance-and-data-safety-by-christian-kvalheim-10gen

