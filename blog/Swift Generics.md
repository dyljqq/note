# Swift Generics

首先来思考一下下面的一个例子：

	 struct Buffer {
	  
	  var count: Int
	  
	  subscript(at: Int) -> Int {
	    get { return 1 }
	  }
	  
	}
	
我们实例完一个Buffer对象，然后呢，就可以通过下标来找到对应的值了，看起来没毛病，但是呢，如果需要构建一个String类型的Buffer咋办呢。暴力点的办法是，定义一个StringBuffer，然后把上面的代码copy一份，把下标的返回值设置为String.

	struct StringBuffer {
  
	  var count: Int
	  
	  subscript(at: Int) -> String {
	    get { return "1" }
	  }
	  
	}
	
但这样很蠢有没有，譬如，我如果要一个DoubleBuffer咋办呢，再copy&paste？显然不合适啊。这时，我开了个脑洞，我把返回值设成Any不就啥事都没了？

	struct AnyBuffer {
	  var array: [Any]
	  
	  var count: Int {
	    get { return array.count }
	  }
	  
	  init(array: [Any]) {
	    self.array = array
	  }
	  
	  subscript(_ index: Int) -> Any {
	    get { return self.array[index] }
	    set { self.array[index] = newValue }
	  }
	}
	
这样不管是什么Int, Double还是String都可以包装进去而不报错。但是新的问题又来了，那就是解包的时候容易出问题，譬如:
	
	var words: AnyBuffer = AnyBuffer(array: ["12", "34", 56])
	words[0] = 42
	print(words)
	let word = words[2] as! String
	print(word)
	
这里就会报一个:

	Could not cast value of type 'Swift.Int' (0x100532750) to 'Swift.String' (0x100534888).
	
的error。

因此swift的Any跟OC的运行时一样，有很多的不确定性，因此应该尽量避免这种运行时的特性，而是回归到静态，即编译时就能把问题给找到。

使用Any还有个弊端就是，会极大程度的浪费内存，因为我不知道你需要多少的内存，所以我会尽可能多的给你分配足够大的内存空间，但你却用来存Bool。

##### 总结:
	
	1. 使用Any，容易引起crash，徒增不确定性
	2. 浪费内存

接着就引入了泛型的概念。

### 泛型

上面的例子用泛型来定义的话，就是这个样子:
	
	struct Buffer<Element> {
	  var array: [Element]
	  
	  var count: Int {
	    get { return array.count }
	  }
	  
	  init(array: [Element]) {
	    self.array = array
	  }
	  
	  subscript(_ index: Int) -> Element {
	    get { return self.array[index] }
	    set { self.array[index] = newValue }
	  }
	}
	
	// Cannot convert value of type 'Buffer<Any>' to specified type 'Buffer<String>'
	var buffers: Buffer<String> = Buffer(array: ["12", 34])
	
	// Cannot assign value of type 'Double' to type 'String'
	buffers[1] = 123.34
	
你看，这样在编译时，就能把crash扼杀在摇篮里，而且内存的分配上也更加的紧凑一些。