# iOS虚拟内存 (VM Region)

所谓的虚拟内存就是我假装自己拥有这块内存，当实际使用的时候，才会将它与物理地址进行映射。当物理内存不足时，OSX上系统会将不活跃的内存块写入硬盘，称为swapping out。iOS上则会通知App清理内存，也就是Memory Warning。

### 内存分页

iOS把虚拟内存每4KB划分为一个Page。

三种状态

1. 活动内存页（active pages）
2. 非活动内存页 (inactive pages)
3. 可用内存页 (free pages)：没有关联到内存页的物理内存页集合

or

1. Nonresident: 没被映射到内存里
2. Resident & Clean: 基于readonly文件而被加载到内存中的Page（如framework）
3. Resident & Dirty: 非clean的Page。(如alloc在堆上的内存空间)

Virtual Size >= Resident Size + Swapped Size >= Dirty Size + Swapped Size

### VM Object

属性:
	
1. Resident Pages: A list of the pages of this region that are currently resident in physical memory.
2. Size: The size of the region, in bytes.
3. Pager: The pager responsible for tracking and handling the pager of this region in backing store.
4. Shadow: Used for copy-on-write optimizations.
5. Copy: Used for copy-on-write optimizations.
6. Attibutes: Flags indicating the state of various implementation details.


### malloc & calloc

 * malloc分配内存时必须先赋值，所以会直接把虚拟内存关联到物理内存
 * calloc是苹果官方的推荐做法，它会将返回的内存自动清零。
	
	