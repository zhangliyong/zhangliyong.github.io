Title: Logbook

## Introduction
Logbook是用来取代标准库logging的一个log系统，根据官方的介绍它让记log变的有趣，
logbook目前还处于开发阶段。可以参考官方[core feature](https://logbook.readthedocs.org/en/latest/features.html#core-features)

logbook与logging差别比较大，logbook和logging基本都是由：logger, handler,
filter等组件组成，但是在logbook中这些组件之间的关系发生的根本的变化。并且logbook提供
了更多的组件，如：processor。

## New Feature
在logbook中一个非常大的变化是大量使用[stack](https://logbook.readthedocs.org/en/latest/stacks.html),
一开始采用logging的方式去理解logbook，发现很不适应，真正去了解之后，发现这种方式有非常强的灵活性，
可以非常灵活的组织handler，而不用去处理handler与logger的有关系，将logger与handler解耦合。

目前logbook中存在三种stack，分别用来存储Handler, Processor, Flag。
每一句log都会经过这三个stack中的每一个对象处理。假如目前存储handler的stack中目前
有两个handler h1, h2:

    | h1 |
    |____|
    | h2 |
    |____|

那每一句log都会被h1处理完后被h2再处理。

Handler, Processor, Flag必须加到stack中才能启到作用，可以使用 `push_application()` 及 `pop_application()`。

logbook中也提供了`with`来完成对stack的push和pop。

logbook增加了很多的handler，甚至都有将log发到twitter上的handler。


logbook有非常多的特性，相信以后也会增加更多有趣的特性，建议阅读其官方文档：https://logbook.readthedocs.org/en/latest/

## Examples
下面给出一些简单的使用示例，有些是官方文档上给出的。

开始使用logbook可以不用做任何配置：

    :::python
    from logbook import warn
    warn('This is too cool for stdlib')
    [2013-05-18 14:29] WARNING: Generic: This is too cool for stdlib

上面的代码会将log记录到stderr中。是不是非常简单，都不需要设置handler，logbook有非常好的默认配置，
在很多情况下你不需要改动即可直接使用。

使用handler：

    :::python
    from logbook import FileHandler, info

    file_handler = FileHandler('logbook.log', level='INFO')
    with file_handler:
        info('This is logged in a file')

### TestHandler
logbook提供了TestHandler，可以用来测试log，使用非常方便，参考文档：
https://logbook.readthedocs.org/en/latest/api/handlers.html#logbook.TestHandler

### MailHandler
https://logbook.readthedocs.org/en/latest/api/handlers.html#logbook.MailHandler
TODO

### ThreadedWrapperHandler
https://logbook.readthedocs.org/en/latest/api/queues.html#logbook.queues.ThreadedWrapperHandler
TODO

### FingersCrossedHandler
logbook提供了一个特殊的"fingers crossed" handler，这个handler作为一个wrapper，是用来封装其它
handler的，这个handler有一个特殊的功能，它会将所有的log记录到内存中，当某一些log的级别
(debug, info, warning, error)超过FingersCrossedHandler设置的级别时，所有在内存中的log以及后面的log
都将被记录到这个handler中。当log级别没有到达时，所有的log都不会被FingersCrossedHandler处理。

这一handler很适合用在web application中，当某一错误产生时记录相关的request。

FingersCrossedHandler默认设置的级别为ERROR

下面给出两个示例代码：

    :::python
    from logbook import info, error, FingersCrossedHandler, FileHandler
    file_handler = FileHandler('bar.log')
    handler = FingersCrossedHandler(file_handler)
    with handler:
        info('hello info')
        error('hello error')

会在bar.log文件中输出两句log

    :::python
    from logbook import info, error, FingersCrossedHandler, FileHandler
    file_handler = FileHandler('bar.log')
    handler = FingersCrossedHandler(file_handler)
    with handler:
        info('hello info')
        info('hello info2')

不会有任何log输出

使用Processors

    :::python
    import os

    def inject_cwd(record):
        record.extra['cwd'] = os.getcwd()

    with Processor(inject_cwd):
        # all logging calls inside this block in this thread will now
        # have the current working directory information attached.
        ...

**注意**： Processor只有当log被某一个handler处理的时候才会执行，否则processor永远不会招待。

