Title: transfer munin server

当修改某一node的主机名时，修改后此node的所有历史记录都会消失，可以恢复这些历史数据，在munin中所有数据都保存在rrd文件中，此文件在/var/lib/munin中，如：social/services.social-uptime-uptime-g.rrd 是主机名为services.social的其中一个数据文件。当修改了node的主机名时，只需要同时对数据文件重命名即可。

1. 取消munin crontab的执行， cd /etc/cron.d/; sudo mv munin munin.disable
    crontab不会执行/etc/cron.d/下文件名中带有“.”的文件
2. 生命名数据文件
3. 修改munin配置/etc/munin/munin.conf中的node主机名
4. 修改munin crontab执行，5分钟后将会看到更新的结果。

**NOTE**： 改动数据文件前要先取消crontab的执行，否则可能会影响历史数据, 同时数据文件迁移之后，要保证用户munin有对这些rrd文件写的权限。因为用`sudo cp`之后会改变这些文件的owner.

如果要将munin server转移到其它机器，只需要将rrd数据文件复制过去即可。
