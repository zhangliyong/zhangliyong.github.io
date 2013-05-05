Title: python build Dynamic Link Library

当我们安装某些软件，需要链接python的动态库时，如果系统的python版本是静态库的，会提示如下错误：

>/usr/bin/ld: .../lib/libpython2.7.a(abstract.o): relocation R_X86_64_32 against 'a local symbol' can not be used when making a shared object; recompile with -fPIC
>.../lib/libpython2.7.a: could not read symbols: Bad value
>collect2: ld returned 1 exit status

这种情况需要安装动态库版本。

下面介绍自己编译安装动态库的python版本。

##安装
通过ubuntu软件库安装的python版本带有动态链接库，位置为`/usr/lib/libpython<version>.so`,

如果系统中默认的python版本太低，软件库中又没有高版本时，需要手动编译安装。

下面以python2.7.4为例，其它版本类似

    :::bash
    ./configure
    make
    sudo make install

默认情况下，`make`会在当前目录下编译生成一个libpython2.7.a的静态链接库。

如果要生成动态链接库，我们需要在`configure`命令后加选项`--enable-shared`

>Building a shared libpython
>
>Starting with Python 2.3, the majority of the interpreter can be built
>into a shared library, which can then be used by the interpreter
>executable, and by applications embedding Python. To enable this feature,
>configure with --enable-shared.


    :::bash
    ./configure --enable-shared
    make
    sudo make install

通过这种方式会生成动态链接库，并安装到系统库目录下,地址：`/usr/local/lib/libpython2.7.so`

##问题

* 在make的过程可能会失败，提示如下错误：

    >/usr/bin/ld: .../lib/libpython2.7.a(abstract.o): relocation R_X86_64_32 against 'a local symbol' can not be used when making a shared object; recompile with -fPIC
    >.../lib/libpython2.7.a: could not read symbols: Bad value
    >collect2: ld returned 1 exit status

    原因是系统链接库目前下存在一个表态链接库`libpython2.7.a`，可能是之前安装的，

    对于这种情况，我们要把系统原有的Python库的路径从编译参数中除去，让链接器先搜索当前目前，当前路径为”.”，通过设置LDFLAGS，如下：

        :::bash
        $ ./configure --enable-shared LDFLAGS=-L.

    同时建议：如果你之前运行过`make`，那么在下一次运行`make`之前，运行`make clean`

* 安装完成之后运行`python`，可能会提示如下错误：

    >ImportError: libpython2.7.so.1.0: cannot open shared object file: No such file or directory

    这是因为新安装的动态链接库`libpython2.7.so`并不在系统的cache中。

    Linux上需要链接动态库时，系统会从cache文件（/etc/ld.so.cache）中找到此链接库。

    此时需要运行 `sudo ldconfig`更新cache。

##参考
[http://www.cbug.org/2011/11/21/multiple-python-versions-cause-shared-library-mess.html](http://www.cbug.org/2011/11/21/multiple-python-versions-cause-shared-library-mess.html)

[http://blog.csdn.net/huzhenwei/article/details/7339548](http://blog.csdn.net/huzhenwei/article/details/7339548)

[http://linux.101hacks.com/unix/ldconfig/](http://linux.101hacks.com/unix/ldconfig/)
