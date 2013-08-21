Title: locale

当在终端下执行某些操作，提示编码问题时，基本是因为终端的locale环境的编码不支持。

有些终端下默认的LC_\*设置为`C`，可运行`locale`查看，也可查看`/etc/default/locale`，
此时终端环境的默认编码是`ASCII`。

可将其改为`UTF8`编码。

修改方式如下：

1. 用`locale -a`命令查看系统支持的category。
2. 在终端下进行`export LANG=<category>`，此时终端的`LC_*`变量发生了变化。
    如果不想每次手动设置，可将`export LANG=<category>`加到`.bashrc`中。
