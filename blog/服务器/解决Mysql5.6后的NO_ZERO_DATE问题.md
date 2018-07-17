# Incorrect datetime value: '0000-00-00 00:00:00'

当我们的mysql版本是5.6及更高的时候，通常如果datetime里的默认值为'0000-00-00 00:00:00'时，系统会报错。

具体的原因是因为:

	sql_mode中含有NO_ZERO_DATE
	
因此，把这个去掉之后，就能够正常的使用了。

首先查看sql_model:

	select @@sql_model;

如果发现有NO_ZERO_DATE，那么就把这个值去掉；

	SET GLOBAL sql_mode="STRICT_ALL_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ZERO_IN_DATE,NO_AUTO_CREATE_USER";
	
然后退出mysql，执行:
	
	bash mysql.server restart
	
之后就可以正常的访问了。