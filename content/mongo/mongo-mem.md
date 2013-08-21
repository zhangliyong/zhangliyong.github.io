Title: How mongodb use memory


网络上经常有文章说mongo会需要大量内存，那么mongo到低需要多少内存。

MongoDB实际需要的内存大小取决于working set的大小，working set是mongo完成操作所需要的所有文档及索引。对于一个collection而言，如果不需要访问每一条记录，不需要所有的记录都在内存中。working set最好都在内存中，以保证好的性能，如果不都在内存中会出现比较多的page fault。

查看working set大小可用如下命令：`db.runCommand( { serverStatus: 1, workingSet: 1 } )`

serverStatus.mem.resident
The value of resident is roughly equivalent to the amount of RAM, in megabytes (MB), currently used by the database process. In normal use this value tends to grow. In dedicated database servers this number tends to approach the total amount of system memory.

所以如果resident没有超出总的内存大小，此时内存是足够的，当然也要看一下page faults是不是很频繁。

Does MongoDB require a lot of RAM?
Not necessarily. It’s certainly possible to run MongoDB on a machine with a small amount of free RAM.

MongoDB automatically uses all free memory on the machine as its cache. System resource monitors show that MongoDB uses a lot of memory, but its usage is dynamic. If another process suddenly needs half the server’s RAM, MongoDB will yield cached memory to the other process.

Technically, the operating system’s virtual memory subsystem manages MongoDB’s memory. This means that MongoDB will use as much free memory as it can, swapping to disk as needed. Deployments with enough memory to fit the application’s working data set in RAM will achieve the best performance.

