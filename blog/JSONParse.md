# JSON的第三方库分享

### ObjectMapper源码分析
	
在看ObjectMapper源码的时候，我自己尝试着写了一个简易的JSON解析器。代码在DJJSON的ObjMapper里。

首先我们都知道，使用ObjectMapper的时候，我们一定要实现Mappable协议。这个协议里又有两个要实现的方法：
	
	init?(map: Map)
	mutating func mapping(map: Map)
	
使用的时候，只用如下:
	
	struct Ability: Mappable {
  		var mathematics: String?
  		var physics: String?
  		var chemistry: String?
  
  		init?(map: Map) {
    
  		}
  
  		mutating func mapping(map: Map) {
    		mathematics <- map["mathematics"]
    		physics <- map["physics"]
    		chemistry <- map["chemistry"]
  		}
	}
	
然后对应的json如下:
	
	let json = """
	{
	"mathematics": "excellent",
	"physics": "bad",
	"chemistry": "fine"
	}
	"""
	
然后将这段json解析为Ability的Model, 即:
	
	let ability = Mapper<Ability>().map(JSONString: json)
	
这样就完成了JSON数据的解析成Model的过程，这也是我们项目中最频繁出现的场景。那么，我们有想过，为什么这样就能将JSON的数据转化为对应的Model么？为什么会需要有‘<-’这么奇怪的符号，它又是啥意思呢？

首先初看<-的符号，我们的第一感觉就是把右边的值赋给左边的变量，然后我们去看源码，发现这个符号是这个库自定义的一个操作符。在Operators.swift里。

定义如下:
	
	infix operator <-
	
	/// Object of Basic type
	public func <- <T>(left: inout T, right: Map) {
		switch right.mappingType {
		case .fromJSON where right.isKeyPresent:
			FromJSON.basicType(&left, object: right.value())
		case .toJSON:
			left >>> right
		default: ()
		}
	}
	

然后根据不同的泛型类型，这个操作符会进行不同的处理。

接着，我们再看一下map方法。

map方法存在于Mapper类中, 定义如下:

	 func map(JSONString: String) -> M? {
    	if let JSON = Mapper.parseJSONString(JSONString: JSONString) as? [String: Any] {
      		return map(JSON: JSON)
    	}
    	return nil
  	}
  
  	func map(JSON: [String: Any]) -> M? {
    	let map = Map(JSON: JSON)
    	if let klass = M.self as? Mappable.Type {
      	if var obj = klass.init(map: map) as? M {
        	obj.mapping(map: map)
        	return obj
      		}
    	}
    	return nil
  	}
  	
可以看到，在map的方法中，我们最后会调用Mappable协议中定义的mapping方法，来对json数据做出转化。

最后再看一下Map这个类，这个类主要用来处理找到key所对应的value。处理方式如下:
	
	private func valueFor(_ keyPathComponents: ArraySlice<String>, dict: [String: Any]) -> (Bool, Any?) {
    	guard !keyPathComponents.isEmpty else { return (false, nil) }
    
    	if let keyPath = keyPathComponents.first {
      		let obj = dict[keyPath]
      		if obj is NSNull {
        		return (true, nil)
      		} else if keyPathComponents.count > 1, let d = obj as? [String: Any] {
        		let tail = keyPathComponents.dropFirst()
        		return valueFor(tail, dict: d)
      		} else if keyPathComponents.count > 1, let arr = obj as? [Any] {
        		let tail = keyPathComponents.dropFirst()
        		return valueFor(tail, array: arr)
      		} else {
        		return (obj != nil, obj)
      		}
    	}
    
    	return (false, nil)
  	}
  
  	private func valueFor(_ keyPathComponents: ArraySlice<String>, array: [Any]) -> (Bool, Any?) {
    	guard !keyPathComponents.isEmpty else { return (false, nil) }
    
    	if let keyPath = keyPathComponents.first, let index = Int(keyPath), index >= 0 && index < array.count {
      		let obj = array[index]
      		if obj is NSNull {
        		return (true, nil)
      		} else if keyPathComponents.count > 1, let dict = obj as? [String: Any] {
        		let tail = keyPathComponents.dropFirst()
        		return valueFor(tail, dict: dict)
      		} else if keyPathComponents.count > 1, let arr = obj as? [Any] {
        		let tail = keyPathComponents.dropFirst()
        		return valueFor(tail, array: arr)
      		} else {
        		return (true, obj)
      		}
    	}
    
    	return (false, nil)
  	}
  	
其中在处理分隔符上，采用的是递归调用的方式，不过就我们目前项目中，还没有用到过。

上述这几个步骤，就是ObjectMapper的核心方法。我也根据这些步骤，自己实现了一个解析的库。

但是这个只能解析一些最简单的类型，其他的像enum之类的，还需要做一些自定义的转化。主要的数据转化都在Operators文件夹中。


### SwiftyJSON 源码解析

##### 构造器

SwiftyJSON对外暴露的主要的构造器:
	
	public init(data: Data, options opt: JSONSerialization.ReadingOptions = []) throws
	public init(_ object: Any)
	public init(parseJSON jsonString: String)
	
最终调用的构造器为:
	
	fileprivate init(jsonObject: Any)
	
##### 类型

自定义了几个类型:
	
	public enum Type: Int {
		case number
		case string
		case bool
		case array
		case dictionary
		case null
		case unknown
	}
	
##### 存储对象已经何时对JSON进行的解析

* 存储对象:
	
		 /// Private object
	    fileprivate var rawArray: [Any] = []
	    fileprivate var rawDictionary: [String: Any] = [:]
	    fileprivate var rawString: String = ""
	    fileprivate var rawNumber: NSNumber = 0
	    fileprivate var rawNull: NSNull = NSNull()
	    fileprivate var rawBool: Bool = false
	    
	    /// JSON type, fileprivate setter
	    public fileprivate(set) var type: Type = .null
	
	    /// Error in JSON, fileprivate setter
	    public fileprivate(set) var error: SwiftyJSONError?
	
* 解析过程
	
	主要是在object属性的get & set方法中进行。然后将解析后的值存储到上述的属性中去。解析过程中，有个unwrap方法值得我们关注。
	
	unwrap:
		
		/// Private method to unwarp an object recursively
		private func unwrap(_ object: Any) -> Any {
		    switch object {
		    case let json as JSON:
		        return unwrap(json.object)
		    case let array as [Any]:
		        return array.map(unwrap)
		    case let dictionary as [String: Any]:
		        var unwrappedDic = dictionary
		        for (k, v) in dictionary {
		            unwrappedDic[k] = unwrap(v)
		        }
		        return unwrappedDic
		    default:
		        return object
		    }
		}
		
	这个方法根据object的类型，对其进行递归的解析。
	
##### JSON的语法糖

为了统一Array和Dictionary的下标访问的类型，自定义了一个enum类型，JSONKey:
	
	public enum JSONKey {
	    case index(Int)
	    case key(String)
	}
	
	// To mark both String and Int can be used in subscript.
	
	extension Int: JSONSubscriptType {
	    public var jsonKey: JSONKey {
	        return JSONKey.index(self)
	    }
	}
	
	extension String: JSONSubscriptType {
	    public var jsonKey: JSONKey {
	        return JSONKey.key(self)
	    }
	}
	
然后就是喜闻乐见的subscript语法糖:
	
	```
	 let json = JSON[data]
	 let path = [9,"list","person","name"]
	 let name = json[path]
	 ```
	public subscript(path: [JSONSubscriptType]) -> JSON
	
	
	// let name = json[9]["list"]["person"]["name"]
	public subscript(path: JSONSubscriptType...) -> JSON
	
###### 数据的转化

最后就是暴露字段，给开发者使用。比如:
	
	 public var int: Int?
	 public var intValue: Int

每个类型都有optional和unoptional。

### Swift 4.0及以后的JSON解析

首先我们知道，在Swift4.0以前，JSON数据解析成Model是多么的繁琐。举个例子:
	
	/// Swift 3.0
	if let data = json.data(using: .utf8, allowLossyConversion: true),
	  let dict = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
	  print("name: \(dict["name"])")
	}
	/// 我们只能获取到json对应的dict，至于转换成model的话，还是需要采用上面的方式，本质都是递归转化，即key与property的对应转化。
	
那么，在swift4.0后，我们可以怎么做呢。如下:

	struct DJJSON<T: Decodable> {
  
	  fileprivate let data: Data
	  
	  init(data: Data?) {
	    if let data = data {
	      self.data = data
	    } else {
	      self.data = Data()
	    }
	  }
	  
	  init(jsonString: String) {
	    let data = jsonString.data(using: .utf8, allowLossyConversion: true)
	    self.init(data: data)
	  }
	  
	  func decode() -> T? {
	    do {
	      let decoder = JSONDecoder()
	      decoder.keyDecodingStrategy = .convertFromSnakeCase
	      let result = try decoder.decode(T.self, from: data)
	      return result
	    } catch let error {
	      print("error: \(error)")
	    }
	    return nil
	  }
	  
	}
	
	if let r = DJJSON<GrocerProduct>(jsonString: json).decode() {
	  print("result: \(r.ability?.mathematics)")
	  print("imageUrl: \(r.imageUrl)")
	}
	
我们只要保证转化的model是遵守Codable协议的即可。至于Key跟Property的转化，苹果默认就帮我做了。那么有的朋友就要问了，那怎么自定义Key呢，苹果给我们提供了一个enum叫CodingKeys，
我们只要在这个里面做自定义就行了，默认的话就是key与property是对应的。如：
	
	private enum CodingKeys: String, CodingKey {
	    case mathematics = "math"
	    case physics, chemistry
	}
	
那么问题又来了，有些字段是蛇形的，像什么image_url，有没有办法不自己做自定义就能搞定呢，诶，还真有，那就是在swift4.1中提供的这个convertFromSnakeCase。
	
	// 完成image_url与imageUrl的转化
	decoder.keyDecodingStrategy = .convertFromSnakeCase
	
那么，这个是怎么实现的呢，我们很好奇，因为感觉自己也可以做这个转化啊，是不是easy game。我们去看swift的源码:
	
	fileprivate static func _convertFromSnakeCase(_ stringKey: String) -> String {
            guard !stringKey.isEmpty else { return stringKey }
        
            // Find the first non-underscore character
            guard let firstNonUnderscore = stringKey.index(where: { $0 != "_" }) else {
                // Reached the end without finding an _
                return stringKey
            }
        
            // Find the last non-underscore character
            var lastNonUnderscore = stringKey.index(before: stringKey.endIndex)
            while lastNonUnderscore > firstNonUnderscore && stringKey[lastNonUnderscore] == "_" {
                stringKey.formIndex(before: &lastNonUnderscore)
            }
        
            let keyRange = firstNonUnderscore...lastNonUnderscore
            let leadingUnderscoreRange = stringKey.startIndex..<firstNonUnderscore
            let trailingUnderscoreRange = stringKey.index(after: lastNonUnderscore)..<stringKey.endIndex
        
            var components = stringKey[keyRange].split(separator: "_")
            let joinedString : String
            if components.count == 1 {
                // No underscores in key, leave the word as is - maybe already camel cased
                joinedString = String(stringKey[keyRange])
            } else {
                joinedString = ([components[0].lowercased()] + components[1...].map { $0.capitalized }).joined()
            }
        
            // Do a cheap isEmpty check before creating and appending potentially empty strings
            let result : String
            if (leadingUnderscoreRange.isEmpty && trailingUnderscoreRange.isEmpty) {
                result = joinedString
            } else if (!leadingUnderscoreRange.isEmpty && !trailingUnderscoreRange.isEmpty) {
                // Both leading and trailing underscores
                result = String(stringKey[leadingUnderscoreRange]) + joinedString + String(stringKey[trailingUnderscoreRange])
            } else if (!leadingUnderscoreRange.isEmpty) {
                // Just leading
                result = String(stringKey[leadingUnderscoreRange]) + joinedString
            } else {
                // Just trailing
                result = joinedString + String(stringKey[trailingUnderscoreRange])
            }
            return result
        }
        
真的写的特别精炼跟严谨好吧，学习一下这个。

到这里，就结束了，谢谢大家。