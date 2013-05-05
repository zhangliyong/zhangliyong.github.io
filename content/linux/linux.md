Title: Linux


##Linux TCP Performance Tuning
There are two ways to change tcp parameters.

1. change the value of parameter files in /proc/sys/net/
   e.g. increase the value of somaxconn
        `echo 1024 > /proc/sys/net/core/somaxconn`
   when the server restart, the parameter will restore.

2. change the vlaue in /etc/sysctl.con, and run `sudo sysctl -p` to apply the changes immediately,
   this can change the value permanently.


###Parameters

* /proc/sys/fs/file-max: The maximum number of concurrently open files.
* /proc/sys/net/ipv4/tcp_max_syn_backlog: Maximum number of remembered connection requests, which are still did not receive an acknowledgment from connecting client. The default value is 1024 for systems with more than 128Mb of memory, and 128 for low memory machines. If server suffers of overload, try to increase this number.
* /proc/sys/net/core/somaxconn: Limit of socket listen() backlog, known in userspace as SOMAXCONN. Defaults to 128. The value should be raised substantially to support bursts of request. For example, to support a burst of 1024 requests, set somaxconn to 1024.
