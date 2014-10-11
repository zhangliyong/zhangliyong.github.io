Title: Hight Throughput Web Server Tunning
Date: 2014-10-11
Tags: Linux, sysadmin, nginx, server


## Performace analysis
how to find the bottleneck of the server performace.

Check out this fabulous pic from <http://www.brendangregg.com/linuxperf.html>
![linux_observability_tools](http://www.brendangregg.com/Perf/linux_observability_tools.png)

and this great slices: <http://www.slideshare.net/brendangregg/linux-performance-tools>

First you need to monitor you server and services, you can use munin, there are a lot of options.

When the service slow down, I would login to the service, using the following tools:

1. htop

    [htop](http://hisham.hm/htop/index.php) is great, it's like `top`, but better, I highly recommend this tool.

    ![htop](http://hisham.hm/htop/htop-1.0-screenshot.png)

    watch the `load`, if `load` > number of CPUs, may mean CPU saturation

2. vmstat

        $ vmstat 1
        procs -----------memory---------- ---swap-- ...
        r  b   swpd   free   buff  cache   si   so ...
        9  0      0 29549320  29252 9299060   0    ...
        2  0      0 29547876  29252 9299332   0    ...
        4  0      0 29548124  29252 9299460   0    ...
        5  0      0 29548840  29252 9299592   0    ...

    The procs data reports the number of processing jobs waiting to run and allows you to determine if there are processes “blocking” your system from running smoothly.

    The `r` column displays the total number of processes waiting for access to the processor. The `b` column displays the total number of processes in a “sleep” state.

    I usually see `r` value, if it's big, it means the server is in a high load.

    For other data meaning, ref: <https://www.linode.com/docs/uptime/monitoring/use-vmstat-to-monitor-system-performance>

3. iostat iotop

    Block I/O status

        $ iostat -xmdz 1

    1st output is since boot.
    For more information refer [24 iostat, vmstat and mpstat Examples for Linux Performance Monitoring](http://www.thegeekstuff.com/2011/07/iostat-vmstat-mpstat-examples/)

    [iotop](http://guichaz.free.fr/iotop/) can show which process use most I/O.

    ![iotop](http://guichaz.free.fr/iotop/iotop_big.png)

4. pidstat

    Very useful process stats. eg, by-thread, disk I/O:

5. iftop

    [iftop](http://www.ex-parrot.com/pdw/iftop/) show the network usage with other hosts.

    ![iftop](http://www.ex-parrot.com/pdw/iftop/iftop_normal.png)

    ![iftop](http://www.ex-parrot.com/pdw/iftop/iftop_ports.png)


## Nginx tunning

somaxconn

fs-max
