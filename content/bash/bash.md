Title: Bash

##alias
对于一些比较常用的长命令可以用alias做一个别名，以后可以直接用别名操作。

e.g. 在.bashrc中加入

    :::bash
    alias servername='ssh sns@hostname'

执行：

    :::bash
    $ servername
即可登陆到hostname机器。

##rsync
大家常用rsync同步数据，有些数据是不需要同步的，可以用 --exclude 选项。

e.g.

    :::bash
    rsync -avz --exclude ".*" --exclude "dbconfig.py" src user@hostname:/dest

    --exclude ".*" 不会同步以"."开头的文件或文件夹，不会同步.git目录（.git目录是比较大的，不建议同步）。

##mail

所有crontab任务的运行结果都会输出到mail中，可以随时查看每个任务的运行情况。


##tmux

工作中经常ssh到远程服务器，有时需要在远程服务器中开启多个终端，

* 一种办法是在本地开启多个终端，分别远程到服务器。
* 还有一种方式是利用[tmux](http://tmux.sourceforge.net/)。

install:

    :::bash
    $sudo apt-get install tmux

basic usage:

    <C-b p> go to previous window
    <C-b n> go to next window
    <C-b c> create a new window
    <C-b 1> go to No.1 window
    <C-b d> detach this tmux session

tmux 的功能非常强，但命令较多，学习成本较高，可以先使用上面几个命令。

推荐介绍视频: http://happycasts.net/episodes/41?autoplay=true


##ssh

今天搞清楚了ssh的标准输入输出，下面是ssh命令的使用方式

    ssh [-1246AaCfgKkMNnqsTtVvXxYy] [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
        [-e escape_char] [-F configfile] [-I pkcs11] [-i identity_file]
        [-L [bind_address:]port:host:hostport] [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option]
        [-p port] [-R [bind_address:]port:host:hostport] [-S ctl_path] [-W host:port]
        [-w local_tun[:remote_tun]] [user@]hostname [command]

最后的`command`是在`hostname`机器上执行`command`命令，那么`command`命令的标准输入输出是远程机器`hostname`上，还是在本地机器上？ 很多初学者可能会认为是远程机器的标准输入输出（本人以前也是这么认为的），其实是在本地机器上。

下面我们做个试验，可以在本地执行远程机器的程序并获得输出结果。

    :::bash
    $echo "local host" | ssh user@hostname "(echo server; cat; echo server)"
    server
    local host
    server

我们用将"local host"输出到标准输出，在hostname机器上`cat`从标准输入获取"local host"并再次输出到标准输出(本地机器的标准输出)。

虽然`command`中的标准输入输出是在本地机器，但`command`中的命令和目录等都是相对于hostname的，与本地机器无法。


fuser
