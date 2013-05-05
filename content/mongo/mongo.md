Title: Mongo

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
