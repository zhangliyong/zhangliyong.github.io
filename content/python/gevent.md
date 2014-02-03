Title: gevent

##Pool
什么时候执行Pool中的任务


用gevent spawn的greenlet何时执行，无论是用group, pool, gevent, 当spawn时，新spawn的greenlet已经处理准备执行状态，
当主进程或其它greenlet sleep或有其它switch操作时，新spawn的greenlet会被执行。

## ref:

Introduction to Gevent: http://blog.pythonisito.com/2012/07/introduction-to-gevent.html

Gevent, Threads, and Benchmarks: http://blog.pythonisito.com/2012/07/gevent-threads-and-benchmarks.html

Gevent and Greenlets: http://blog.pythonisito.com/2012/07/gevent-and-greenlets.html

Greening the Python Standard Library with Gevent: http://blog.pythonisito.com/2012/08/gevent-monkey-patch.html

Building TCP Servers with Gevent: http://blog.pythonisito.com/2012/08/building-tcp-servers-with-gevent.html

Building Web Applications with Gevent's WSGI Server: http://blog.pythonisito.com/2012/08/building-web-applications-with-gevents.html
