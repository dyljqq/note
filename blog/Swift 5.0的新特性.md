# Swift 5.0的新特性

[原文链接](https://www.hackingwithswift.com/articles/126/whats-new-in-swift-5-0)

### Result<T, Error>

普天同庆，swift 5.0将Result类型加入了官方库中。这意味着，我们未来在写比如网络回调，组织数据的时候，可以这样:

	func fetch<T>(result: Result<T, Error>) {
	  switch result {
	  case .success(let data):
	    print("data: \(data)")
	  case .failure(let error):
	    print("error: \(error)")
	  }
	}
	
	let result = Result<String, Error>.success("123")
	fetch(result: result) // data: 123
	
	// 如果是success的话，可以通过下面的方式取值:
	if let s = try? result.get() {
	  print(s) // 123
	}
	
	// 通过闭包，构造result:
	let result = Result { "123" }
	
### 原始字符串

大概就是在前后都加上#符号，可以被判定为是想要表达原始的意思，如:

	let rain = #"The "rain" in "Spain" falls mainly on the Spaniards."#
	print(rain)
	
之前的情况是，双引号会表示为字符串结束，但是加了#后，就被认为，双引号表示原有的意思，而不是字符串结束的标志。

这个在正则表达式中，会比较有用，可以少些一些符号，如:

	let regex1 = "\\\\[A-Z]+[A-Za-z]+\\.[a-z]+"
	
可以写成:

	let regex2 = #"\\[A-Z]+[A-Za-z]+\.[a-z]+"#
	
### 处理enum中的case

我们在枚举enum的时候，很多时候不会枚举完所有的case，因此会加入default，但是这样就会有个问题，就是如果我们后面新加入一个case的话，忘了给这个case加上处理的方式的话，编译器也不会报错，不会给我们做检查，因此，swift加入了一个新功能，叫做: @unknown, 它可以在你新加case的时候提醒你，不要忘了给它加上处理的逻辑:


	enum PPError: Error {
	  case short
	  case obvious
	  case simple
	}
	
	func showOld(error: PPError) {
	  switch error {
	  case .obvious:
	    print("obvious...")
	  @unknown default:
	    print("default...")
	  }
	}
	
	showOld(error: .simple)
	
### 将用try?嵌套的可选值打平

	struct User {
	  var id: Int
	  
	  init?(id: Int) {
	    if id < 1 {
	      return nil
	    }
	    
	    self.id = id
	  }
	  
	  func getMessages() throws -> String {
	    // complicated code here
	    return "No messages"
	  }
	}
	
	let user = User(id: 1)
	let messages = try? user?.getMessages()
	print("\(messages)")
	
swift5之前应该输出的是: String??
现在就只是: String?

### 判断一个数能否被整除

Swift5.0新增了一个方法，可以用来判断:

	let rowNumber = 4

	if rowNumber.isMultiple(of: 2) {
	    print("Even")
	} else {
	    print("Odd")
	}
	
	// 之前我们要这么写:
	
	if rowNumber % 2 == 0 {
		
	} else {
		
	}
	
用上面的方法的话，可以更加的清晰表达条件的意思， 客气可以有编译器帮你检查。

### 用compactMapValues函数展开字典的值

	let times = [
	  "Hudson": "38",
	  "Clarke": "42",
	  "Robinson": "35",
	  "Hartis": "DNF"
	]
	
	let d = times.compactMapValues { Int($0) }
	print(d)
	
这个方法可以将value为nil的键值去除，并返回一个新的字典。

### 用count(where:)函数计算满足某个条件的序列的个数

	let scores = [100, 80, 85]
	let passCount = scores.count { $0 >= 85 } // 2
