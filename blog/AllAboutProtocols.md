# All About Protocols

### Protocol Composition

	protocol Animalable {
  		func eat() -> String
	}

	protocol Growable {
  		var age: Int { get }
	}

	func printAgeOfAnimal(animal: Animalable & Growable) {
  		print("\(animal.age), \(animal.eat())")
	}

	class Animal: Animalable, Growable {
  
  		var age: Int {
    		return 18
  		}
  
  		func eat() -> String {
    		return "eat"
  		}
  
	}

	printAgeOfAnimal(animal: Animal())
	
	
### Generic Protocol

You cannot treat protocols with associated types like regular protocols and declare them as standalone variable types.

	// Generic Protocol

	protocol Storable {
  
  		associatedtype Store
  
  		init(_ value: Store)
  
  		func getStore() -> Store
  
	}

	struct IntStore: Storable {
  
  		typealias Store = Int
  
  		private let _store: Int
  
  		init(_ value: Store) {
    		self._store = value
 		}
  
  		func getStore() -> Int {
    		return _store
  		}
  
	}

	struct StringStore: Storable {
  
  		typealias Store = String
  
  		private let _store: String
  
  		init(_ value: Store) {
    		self._store = value
  		}
  
  		func getStore() -> String {
    		return _store
  		}
  
	}

	let intStore = IntStore(5)
	intStore.getStore()

	let stringStore = StringStore("dyl")
	stringStore.getStore()

	// As you have seen this won't compile because Storable has associated type.

	// error... protocol 'Storable' can only be used as a generic constraint because it has Self or associated type requirements
	//var someStore: Storable = arc4random() % 2 == 0 ? intStore :  stringStore
	//let x = someStore.getStore()

	// In swift, all types must be fixed at compile time

	func printStoreValue<S: Storable>(store: S) {
  		let x = store.getStore()
  		print("x: \(x)")
	}

	printStoreValue(store: intStore)
	printStoreValue(store: stringStore)
	
	// Another implemention
	
	struct Store<T>: Storable {
  
  		typealias S = T
  
  		private let _store: T
  
  		init(_ value: T) {
    		self._store = value
  		}
  
  		func getStore() -> T {
    		return self._store
  		}

	}

	print("x: \(Store<String>("dyl"))")
	print("x: \(Store<Int>(5))")
	
	
### 关于协议在熊猫优选中的实现

在熊猫优选的用户数据那块，我采用了协议的方式，来将共有的方法给抽象出来。

比如， 在User, ThirdUser中都会有对这两个model进行转换的方法， 两个方法分别做的工作是将model to dict & dict -> model。

所以我写了一个协议叫做convertable:

	protocol Convertable: Mappable {
	
		// model -> dict
  		func toDict() -> [String: Any]
  		
  		// dict -> model
  		static func build(_ dict: [String: Any]) -> Self?
	}
	
	extension Convertable {
  
  		func toDict() -> [String: Any] {
    		return toJSON()
  		}
  
  		static func build(_ dict: [String: Any]) -> Self? {
    		return Mapper<Self>().map(JSON: dict)
  		}
  
	}
	
这样所以实现convertable协议的model，就都可以使用toDict和build的方法，这里我提供了默认实现，是因为User, ThirdUser，ThirdInfo所做的工作都是一样的。

然后抽象出了一个Userable协议，给UserUtils和ThirdUserUtils使用。这个协议也是把一些共有的方法给抽象出来，因为这些共有方法的实现逻辑都是相同的，结合刚才定义的convertable协议，给了默认的实现。 具体如下:
	
	protocol Userable {
  
  		associatedtype Element: Convertable
  
  		static var user: Observable<Element?> { get set }
  
  		static var storeKey: String { get }
  
  		static func get() -> Element?
  
  		static func save(_ user: Element)
  
  		static func delete()
  
	}

	extension Userable {
  
  		static func get() -> Element? {
    		if let dict = UserDefaults.standard.dictionary(forKey: storeKey) {
      			return Element.build(dict)
    		}
	    	return nil
  		}
  
  		static func save(_ user: Element) {
    		self.user.value = user
    
    		UserDefaults.standard.set(user.toDict(), forKey: storeKey)
    		UserDefaults.standard.synchronize()
  		}
  
  		static func delete() {
    		self.user.value = nil
    
    		UserDefaults.standard.set(nil, forKey: storeKey)
    		UserDefaults.standard.synchronize()
  		}
	}
	
	// 使用
	struct ThirdUserUtils: Userable {
  
  		typealias Element = ThirdUser
  
  		static var storeKey: String = UserDefaultKey.thirdUser
  
  		static var user: Observable<ThirdUser?> = Observable(get())
  		
  		// 其他功能
  		static var isBind: Bool {
    		return !(get()?.needPhoneBind ?? true)
  		}
	}
	
通过面向协议编程可以把一些共有的逻辑都抽象出来，让代码的实现上更加的简洁，可维护性更高。