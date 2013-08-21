Title: Mongo


## query after update slow

这两天有一个接口的速度非常慢，主要是执行一条查询语句非常慢，有时耗时达200秒，于是找到了这条查询语句单独在mongo shell中执行，在mongo shell中执行并不慢，慢慢调试后最终找到问题，原因是在查询语句执行之前执行了两次更新语句。

利用pymongo执行更新时，如果不设置safe=True，mongo会及时返回函数调用，但更新并没有真正执行完，mongo进程在后台继续执行，所以当接着执行查询时，此时更新没有结束，数据库会处于lock状态，查询等待数据库解锁，所以查询非常慢。

把更新语句去除后，查询恢复正常。

##Concurrency

MongoDB global lock to ga


##Tips

### If Write Heavy

Global Lock is Global
As you probably know, MongoDB has a global lock. The longer your writes take, the higher your lock percentage is. Updating documents that are in RAM is super fast.

Updating documents that have been pushed to disk, first have to be read from disk, stored in memory, updated, then written back to disk. This operation is slow and happens while inside the lock.

Updating a lot of random documents that rarely get updated and have been pushed out of RAM can lead to slow writes and a high lock percentage.

More Reads Make For Faster Writes
The trick to lowering your lock percentage and thus having faster updates is to query the document you are going to update, before you perform the update. Querying before doing an upsert might seem counter intuitive at first glance, but it makes sense when you think about it.

The read ensures that whatever document you are going to update is in RAM. This means the update, which will happen immediately after the read, always updates the document in RAM, which is super fast. I think of it as warming the database for the document you are about to update.

http://www.mongotips.com/b/lower-lock-and-number-of-slow-queries/
