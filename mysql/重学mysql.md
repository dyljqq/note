# 重学mysql

### mysql事物

##### 事务的四个特性
	
* 原子性(Atomicity): 出错回滚机制
* 一致性(consistency): 数据库的完整性不被破坏
* 隔离性(isolation): 允许多个并发事务同时修改数据的能力。1. 未提交 2. 读提交 3. 可重复读 4. 串行化
* 持久性(durability): 修改的结果，永久存在

##### 事务处理的两种方法

1. begin, rollback, commit
2. 表引擎 = InnoDB生效, set autocommit = 1 // 0: 禁止自动提交 1: 开启自动提交

	select @@autocommit; // 获取对应的值
	
### Alter

	alter table tablename drop name;
	alter table tablename add name int after c;
	alter table tablename modify name varchar(20);
	alter table tablename alter name set DEFAULT 1000;
	
	// 修改表名
	alter table tablename rename to tn;