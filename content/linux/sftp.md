Title: sftp in ssh config
Tags: fabric, python, ssh, sftp
Date: 2014-02-17 09:11

今天在使用 fabric 中的 `put` 函数上传文件到服务器时，抛出 `Connection closed` 的异常，Google 之后发现 `put` 使用 `sftp` 进行上传，于是使用 `sftp` 连接服务器：

    $ sftp user@domain.org 
    Connecting to domain.org... 
    user@domain.org's password: 
    subsystem request failed on channel 0 
    Connection closed 

发现连接失败.

解决方案：

https://forums.gentoo.org/viewtopic-t-802682-start-0.html

In your /etc/ssh/sshd_config (not ssh_config) file, you probably have a line like this: 

Code:

    Subsystem sftp /usr/lib/misc/sftp-server


If so, it's the cause of this error message. That's especially true if your sftp user is logging into a chrooted environment, where "/usr/lib" probably does not exist. My own sftp server is configured this way. 

However, SSHD has the sftp functionality built-in and does not need to execute an external "helper" program like that. So, if you have a line like the above, it can be fixed by changing it to: 

Code:

    Subsystem sftp internal-sftp
