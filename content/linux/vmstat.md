Title: vmstat

最近在分析mongo的性能问题，发现mongo所在机器的io比较频繁。

使用vmstat命令查看，发现b（The number of processes in uninterruptible sleep）这一列的数量比较大，持续在4左右。
随后查询uninterruptible sleep状态的意义，引自：http://www.novell.com/support/kb/doc.php?id=7002725

>Processes in a "D" or uninterruptible sleep state are usually waiting on I/O. The ps command shows a "D" on processes in an uninterruptible sleep state. The vmstat command also shows the current processes that are "blocked" or waiting on I/O. The vmstat and ps will not agree on the number of processes in a "D" state, so don't be too concerned. You cannot kill "D" state processes, even with SIGKILL or kill -9. As the name implies, they are uninterruptible. You can only clear them by rebooting the server or waiting for the I/O to respond. It is normal to see processes in a "D" state when the server performs I/O intensive operations. 
>
>If performance becomes an issue, you may need to check the health of your disks. Make sure your firmware and kernel disk drivers are updated. 
>
>In the example above, there is heavy disk activity shown in the "io" columns and the server is currently swapping to disk. The example more likely represents a memory issue, rather than a disk I/O issue. 
>
>There are two ways to find more about the processes in D state.
>
>1. ps -eo ppid,pid,user,stat,pcpu,comm,wchan:32
>This prints a list of all processes where in the last column either a '-' is displayed when the process is running or the name of the kernel function in which the process is sleeping if the process is currently sleeping. This includes also processes which are interruptible. Processes that are in uninterruptible sleep can be determined via the fourth column which would then show a D.
>
>2. echo w > /proc/sysrq-trigger
>This command produces a report and a list of all processes in D state and a full kernel stack trace to /var/log/messages. This shows much more information than the first option described above.


关于vmstat的使用参考：http://www.linuxintheshell.org/2013/05/22/episode-030-vmstat/
