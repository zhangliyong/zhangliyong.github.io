Title: fabric

下面介绍python下的一个用于项目部署的工具[fabric](http://docs.fabfile.org/)，要学习fabric推荐阅读其官方文档，

本文给只给出一个简单的介绍及一些基本的功能。

根据官方文档的介绍:

>Fabric is:

>A tool that lets you execute arbitrary Python functions via the command line;
>A library of subroutines (built on top of a lower-level library) to make executing shell commands over SSH easy and Pythonic.

首先安装fabric `pip install fabric`，安装完fabric之后，系统会多出fab命令。

fab命令在执行时会读取当前目录下的fabfile.py文件，并根据fabric的参数来执行文件中的函数。

fabfile.py

    def hello():
        print("Hello world!")

hello为一个task，执行hello如下：

    $ fab hello
    Hello world!

    Done.

我们看到hello并没有参数，fab也支持给task加参数。


fab可以用于项目部署，服务器管理。它可以通过ssh执行服务器上的shell命令，当然也可以执行本地的shell命令。

例如： local执行本地命令，run执行服务器端命令，sudo以root权限执行服务器端命令。

fab可以通过设置env.hosts变量来在所有host中执行某一task。

fab也提供了一些decorator，如hosts, roles来设置在某些host上执行task。
