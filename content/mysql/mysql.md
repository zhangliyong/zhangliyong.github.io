Title: Mysql 性能调优


## thread cache size
http://www.dbasquare.com/kb/mysql-and-thread-cache-size/


query_cache_type可以设置为0(OFF)，1(ON)或者2(DEMOND)，分别表示完全不使用query cache，除显式要求不使用query cache（使用sql_no_cache）之外的所有的select都使用query cache，只有显示要求才使用query cache（使用sql_cache)


show global status like '';
show global variables like '';

innodb_file_per_table

mysql io 延时计算


##mysql backup

相较前几种方法，备份数据文件最为直接、快速、方便，缺点是基本上不能实现增量备份。为了保证数据的一致性，需要在靠背文件前，执行以下 SQL 语句：

FLUSH TABLES WITH READ LOCK;
也就是把内存中的数据都刷新到磁盘中，同时锁定数据表，以保证拷贝过程中不会有新的数据写入。这种方法备份出来的数据恢复也很简单，直接拷贝回原来的数据库目录下即可。

注意，对于 Innodb 类型表来说，还需要备份其日志文件，即 ib_logfile* 文件。因为当 Innodb 表损坏时，就可以依靠这些日志文件来恢复。


Innodb 表则可以通过执行以下语句来整理碎片，提高索引速度：

ALTER TABLE tbl_name ENGINE = Innodb;
这其实是一个 NULL 操作，表面上看什么也不做，实际上重新整理碎片了。

为了不影响线上业务，实现在线备份，并且能增量备份，最好的办法就是采用主从复制机制(replication)，在 slave 机器上做备份。


##mysql replication

### switch master and slave
**one slave and one master**

* Master: set read lock
          FLUSH TABLES WITH READ LOCK;


* Slave: show processlist;  when you see 'Has read all relay log', it means the slave is updated with master.
         stop slave; reset master;

* chane the code to operate on slave;

* Master: UNLOCK TABLES;
          make the old master to be a slave;
          change master to MASTER_HOST = '10.18.10.21', MASTER_USER = 'sns', MASTER_PASSWORD = '123';

1. 

[mysqld]
log-bin=mysql-bin
server-id=1
After making the changes, restart the server.

Note
If you omit server-id (or set it explicitly to its default value of 0), a master refuses connections from all slaves.

Note
For the greatest possible durability and consistency in a replication setup using InnoDB with transactions, you should use innodb_flush_log_at_trx_commit=1 and sync_binlog=1 in the master my.cnf file.

Note
Ensure that the skip-networking option is not enabled on your replication master. If networking has been disabled, your slave will not able to communicate with the master and replication will fail.



2.

After connecting to the server as root, you can add new accounts. The following statements use GRANT to set up four new accounts:

mysql> CREATE USER 'monty'@'localhost' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'monty'@'localhost'
    ->     WITH GRANT OPTION;
mysql> CREATE USER 'monty'@'%' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'monty'@'%'
    ->     WITH GRANT OPTION;
mysql> CREATE USER 'admin'@'localhost';
mysql> GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
mysql> CREATE USER 'dummy'@'localhost';
The accounts created by these statements have the following properties:

Two of the accounts have a user name of monty and a password of some_pass. Both accounts are superuser accounts with full privileges to do anything. The 'monty'@'localhost' account can be used only when connecting from the local host. The 'monty'@'%' account uses the '%' wildcard for the host part, so it can be used to connect from any host.

It is necessary to have both accounts for monty to be able to connect from anywhere as monty. Without the localhost account, the anonymous-user account for localhost that is created by mysql_install_db would take precedence when monty connects from the local host. As a result, monty would be treated as an anonymous user. The reason for this is that the anonymous-user account has a more specific Host column value than the 'monty'@'%' account and thus comes earlier in the user table sort order. (user table sorting is discussed in Section 6.2.4, “Access Control, Stage 1: Connection Verification”.)

The 'admin'@'localhost' account has no password. This account can be used only by admin to connect from the local host. It is granted the RELOAD and PROCESS administrative privileges. These privileges enable the admin user to execute the mysqladmin reload, mysqladmin refresh, and mysqladmin flush-xxx commands, as well as mysqladmin processlist . No privileges are granted for accessing any databases. You could add such privileges later by issuing other GRANT statements.

The 'dummy'@'localhost' account has no password. This account can be used only to connect from the local host. No privileges are granted. It is assumed that you will grant specific privileges to the account later.

The statements that create accounts with no password will fail if the NO_AUTO_CREATE_USER SQL mode is enabled. To deal with this, use an IDENTIFIED BY clause that specifies a nonempty password.

To check the privileges for an account, use SHOW GRANTS:

mysql> SHOW GRANTS FOR 'admin'@'localhost';
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+


16.1.1.5. Creating a Data Snapshot Using mysqldump  :  http://dev.mysql.com/doc/refman/5.1/en/replication-howto-mysqldump.html

Obtaining the Replication Master Binary Log Coordinates : http://dev.mysql.com/doc/refman/5.1/en/replication-howto-masterstatus.html


If a slave uses the default host-based relay log file names, changing a slave's host name after replication has been set up can cause replication to fail with the errors Failed to open the relay log and Could not find target log during relay log initialization. This is a known issue (see Bug #2122). If you anticipate that a slave's host name might change in the future (for example, if networking is set up on the slave such that its host name can be modified using DHCP), you can avoid this issue entirely by using the --relay-log and --relay-log-index options to specify relay log file names explicitly when you initially set up the slave. This will make the names independent of server host name changes.
