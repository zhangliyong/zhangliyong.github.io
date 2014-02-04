Title: ack.vim
Slug: vim-ack
Date: 2014-02-04 16:20
Tags: vim, ack, grep
Summary: An ack-vim plugin tutorial

[ack](http://beyondgrep.com/) 是一个类似于grep的工具，专门针对程序员进行了优化，主要用于搜索源代码，默认忽略非代码文件，支持大部分编程语言。在各平台的安装参考其官方网站 http://beyondgrep.com/ 。

[ack.vim](https://github.com/mileszs/ack.vim) 是ack的vim插件，可在vim下直接使用ack。

ack可通过配置文件调整搜索行为，如增加新编程语言的技术等。

类似于大部分unix程序，ack有全局配置(/etc/ackrc)，用户配置(~/.ackrc)，工程配置(.ackrc)等，可参考其manpage。

下面列出本人的用户配置(~/.ackrc):

    --smart-case
    --sort-files
    --type-set=rst:ext:rst,txt
    --type-set=md:ext:mkd,md,markdown
    --type-set=dotfile:match:/^\..+/
    --nodotfile

增加对Markdown和reStructuredText文件的支持，并忽略所有以"."开头的隐藏文件。
