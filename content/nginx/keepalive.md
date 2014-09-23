Title: HTTP keep-alive

今天在阅读[Django performance tips](http://jacobian.org/writing/django-performance-tips/)时发现关闭keepalive可以提高效率，原文如下：

>Turn off KeepAlive
>I don’t totally understand how KeepAlive works, but turning it off on our Django servers increased performance by something like 50%. Of course, don’t do this if the same server is also serving media… but you’re not doing that, right?

HTTP keep-alive即是HTTP persistent connection，维基百科有详细说明：http://en.wikipedia.org/wiki/HTTP_persistent_connection

如果使用keep-alive功能，多个http请求会使用同一个tcp连接，这样可节省多次建立连接的时间及资源消耗，

下图显示了是否使用keep-alive功能的tcp连接对比图：

![persistent connection](http://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/HTTP_persistent_connection.svg/500px-HTTP_persistent_connection.svg.png)

http 1.0默认不开启，可进行指定，http 1.1默认开启。

上面我们看到启用keep-alive可节省多次建立连接的时间，但是服务器端要保持连接状态(nginx默认保持74s)，
这样会影响服务器端的性能。 而且目前网络带宽比较大，建立连接的延时比较少，
所以keep-alive在很多情况下会导致性能下降。这就验证了一开始那篇文章指出的在django servers中关闭keep-alive
功能可大约提升50%的性能。

所以建议关系keep-alive功能，除非有特殊需求。

下面介绍如何nginx中关系keep-alive功能

[nginx文档](http://wiki.nginx.org/HttpCoreModule#keepalive_timeout)中有详细说明:

>keepalive_timeout
>
>Syntax: keepalive_timeout timeout [ header_timeout ]
>
>Default:    75s
>
>Context:    http
>            server
>            location
>
>Reference:  keepalive_timeout
>
>The first parameter assigns the timeout for keep-alive connections with the client. The server will close connections after this time.
>
>The optional second parameter assigns the time value in the header Keep-Alive: timeout=time of the response. This header can convince some browsers to close the connection, so that the server does not have to. Without this parameter, nginx does not send a Keep-Alive header (though this is not what makes a connection "keep-alive").

如果我们要关闭keep-alive功能，可在http, server或location中设置`keepalive_timeout  0;`

如：

    server {
      listen          port;
      server_name     address;
      access_log      /var/log/nginx/mysite-access.log ;
      error_log       /var/log/nginx/mysite-error.log ;
      keepalive_timeout  0;
      location / {
        ........
      }
    }

下图给出了keepalive_timeout设置前后，http请求的header中connection的变化：

![keepalive](/images/nginx/keepalive/keepalive.png)

设置`keepalive_timeout  0;`之后：

![notalive](/images/nginx/keepalive/notalive.png)


笔者并没有对keep-alive做相应性能方面的benchmark，所以不确定keep-alive对性能的影响，而且keep-alive对性能的影响也与应用场景有关。
