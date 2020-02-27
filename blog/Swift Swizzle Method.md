# Swift Swizzle Method

如何在swift中实现方法混淆呢:

	func swizzleMethod(_ cls: AnyClass, origin: Selector, swizzled: Selector) {
	   guard let originMethod = class_getInstanceMethod(cls, origin),
	    let swizzledMethod = class_getInstanceMethod(cls, swizzled) else {
	        return
	    }
	
	    let didAddMethod = class_addMethod(cls, origin, method_getImplementation(originMethod), method_getTypeEncoding(originMethod))
	    if didAddMethod {
	      class_replaceMethod(cls, swizzled, method_getImplementation(originMethod), method_getTypeEncoding(originMethod))
	    } else {
	      method_exchangeImplementations(originMethod, swizzledMethod)
	    }
	}
	
然后在执行的时候，需要同步的执行，因此需要一个dispatch_once，但是在swift中并没有提供这个方法，因此，自己实现:

	extension DispatchQueue {
	    private static var _onceTracker = [String]()
	
	    class func once(token: String, block: @escaping () -> Void) {
	      objc_sync_enter(self)
	      defer {
	        objc_sync_exit(self)
	      }
	
	      if _onceTracker.contains(token) {
	          return
	      }
	      _onceTracker.append(token)
	      block()
	    }
	}
	
然后我们在hook的时候，就可以着么做:

	DispatchQueue.once(token: "com.dyl.vc") {
      swizzleMethod(UIViewController.self, origin: #selector(UIViewController.present(_:animated:completion:)), swizzled: #selector(UIViewController.swizzledPresent(_:animated:completion:)))
    }