# iOS多线程不安全问题

### Property

	@property (atomic, strong) NSString *userName;
	
我们都知道atomic是原子性的，它可以保证，这个属性在多线程的时候是安全的，但是会有一定的性能消耗。所以在写iOS的时候，会尽量采用nonatomic。

property又可以分成值类型和引用类型，如userName就是引用类型。而int a；就是值类型。

当我们讨论多线程安全的时候，其实是在讨论多个线程同时访问一个内存区域的安全问题。

### 不安全的定义

	 A piece of code is thread-safe if it manipulates shared data structures only in a manner that guarantees safe execution by multiple threads at the same time
	 
	 
然后引入地址总线，就是我们只有一根地址总线来访问某一块内存，地址总线的大小跟系统有关。

	结论一：内存的访问时串行的，并不会导致内存数据的错乱或者应用的crash。

	结论二：如果读写（load or store）的内存长度小于等于地址总线的长度，那么读写的操作是原子的，一次完成。比如bool，int，long在64位系统下的单次读写都是原子操作。
	
### 如何做到安全

就是控制访问的力度

如：
	
	self.userName = self.userName + @"112111"
	
在多线程访问的时候，这个也不是现成安全的。因为这个编译器需要做三步，即load, add, store三步，任何一步都可能会被篡改。因此需要保证这个语句是多线程安全的，即给这个语句加锁。这里用Dispatch会比较顺手（个人而言）


原文链接: [iOS多线程到底不安全在哪里？](http://mrpeak.cn/blog/ios-thread-safety/)