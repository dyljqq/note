# 日志

## InnoDB日志

WAL技术，即Write-Loggin Ahead，叫做日志先行，先写日志，再写磁盘。

#### undo log

#### redo log

首先这个redo log有啥用呢，它有个能力叫crash-save，就是数据库异常宕机了后，我们根据这个日志可以恢复之前的操作。

redo log首先是InnoDB所独有的，跟mysql的server层没啥关系，因为InnoDB是通过插件的形式，与mysql进行衔接的。redo log大小固定，比如可以配置4个1GB的文件，然后根据两个指针，分别叫做check point跟write pos，指针中间的就是可以写入的部分。当两个指针重合的时候，就需要将check point迁移一定的位置，并将移动的空间中的数据给清空。从头开始写入，写到末尾后，再回到开头位置循环写入。

ps：擦除记录前，要把数据写入到数据文件。

### binlog

mysql层的日志，没有crash-save的能力。写入日志的方式是追加写入。

### 执行的过程

拿这个sql语句举例:

	update table set c = c + 1 where ID=2; // ID是主键
	
首先，我们知道这是一条更新的语句，那么它在mysql中是怎么执行的呢?

1. 通过主键去查找ID=2的数据，如果在内存中，就直接取出来，如果不在，则从磁盘中读取一页的数据到内存中，然后返回给执行器。
2. 执行器拿到了这个数据c，然后给c值加上1，得到新的一行数据给引擎接口
3. 引擎将这行数据更新到内存中去，同时将这个操作记录写到redo log，此时redo log处于prepare状态
4. 执行器生成这个操作的binlog，然后告知执行器，可以提交事务了。
5. 执行器调用引擎的提交事务的接口，引擎把redo log的prepare状态改成提交的状态，更新完成。

需要注意的是，redo log与bin log要保持逻辑上的一致。