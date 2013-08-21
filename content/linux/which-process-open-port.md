Title: Find out which process open a linux port

最近在调mongodb的性能，发现currentop中有很多长时间运行的查询，从currentop中可以看到查询来源ip:port。

那么可以到ip机器上查询port对应的进程号，进而找到发出此查询的应用。

根据port来查询进程号有多种方案：

1. netstat， `sudo netstat -anp | grep <port>`

    关于netstat的使用参考：http://www.thegeekstuff.com/2010/03/netstat-command-examples/

2. fuser，找到使用tcp 7000端口号的进程：`sudo fuser 7000/tcp`

3. lsof

        lsof -i :portNumber
        lsof -i tcp:portNumber
        lsof -i udp:portNumber
        lsof -i :80

通过这几种方式找到进程号后，可以利用`ps -eaf | grep <pid>`找到此进程的执行命令，
并可以通过`/proc/<pid>/cwd`找到此进程的执行目录。

参考：http://www.cyberciti.biz/faq/what-process-has-open-linux-port/
