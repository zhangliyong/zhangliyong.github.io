Title: munin

##Writing plugins

global attribute: http://munin-monitoring.org/wiki/protocol-config


redis munin 有改动，总是说Redis找不到，一会儿一下问题，做一个patch

mulitgraph: http://munin-monitoring.org/wiki/protocol-multigraph


## fw_conntract fw_forwarded_local timeout
配置好munin之后，fw_conntrack总是报警，读不到数据，主要原因是执行fw_conntrack超时，munin plugin的默认超时时间是10s，超时主要是因为`cat /proc/net/ip_conntrack`，对于网络请求少的服务器，此语句会很快执行完，但对于网络请求比较多的服务器，此语句耗时可能要超过30s。

Google的相应问题，此问题早已被人解决，解决方案见如下链接：
http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=565565

主要就是用`conntrack -L` 代替`cat /proc/net/ip_conntrack`，要先安装`sudo apt-get install conntrack`


## limits
limit 用于检查每个plugin的field的值是否超出设定的warning和critical，并做出相应的警报。

warning和critical是运行插件config输出的每个filed的warning和critical来设置的。

有时我们在`/etc/munin/plugin-conf.d/`中会看到`env.warning value`，这是因为插件会读取`env.warning`的值，并根据此值设置每个field的warning。如果插件不读取`env.warning`的值，即使设置也不会启作用，munin不会自动设置。

关于warning, critical的设置可参考: [{fieldname}.warning](http://munin-monitoring.org/wiki/fieldname.warning), [{fieldname}.critical}](http://munin-monitoring.org/wiki/fieldname.critical)

http://munin-monitoring.org/wiki/protocol-config

http://munin-monitoring.org/wiki/munin-man#munin-html
