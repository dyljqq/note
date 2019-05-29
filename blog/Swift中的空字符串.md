# Swift中的空字符串

[原文链接](https://useyourloaf.com/blog/empty-strings-in-swift/)

首先，我们怎么检测一个字符串是否为空呢。

Swift中有一个属性叫isEmpty

	var isEmpty: Bool { get }
	
	
我们可以去Swift源码中，看到isEmpty的实现:

	public var isEmpty: Bool {
	  return startIndex == endIndex
	}
	
只是去简单的比较了起始点是否与终结点相同.
	
我们可以这样去检测:

	var str = "Hello, playground"

	str.isEmpty // false
	
	str = ""
	str.isEmpty // true
	
但是有个问题是，有的时候我们希望只包含空格这种类型的字符串，也被定义成空字符串，如:

	" ".isEmpty // false
	
因此我们需要写一个方法来做这个，就叫做:

	extension String {
	  var isBlank: Bool {
	    return allSatisfy({ $0.isWhitespace })
	  }
	}
	
	" ".isBlank // true
	
然后如果字符串是个可选值:

	extension Optional where Wrapped == String {
	  var isBlank: Bool {
	    return self?.isBlank ?? true
	  }
	}
	
	let s: String? = "  "
	print("\(s.isBlank)") // true