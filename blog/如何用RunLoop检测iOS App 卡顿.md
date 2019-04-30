# 如何用RunLoop检测iOS App 卡顿

首先本文的思路来自于网上的各种资料。然后搜了半天发现没有swift版的，于是撸了一个。

其实具体的思路非常的简单:

1. 首先创建一个runloop的observer对象:
	
		let info = Unmanaged<Monitor>.passUnretained(self).toOpaque()
	    var context: CFRunLoopObserverContext = CFRunLoopObserverContext(version: 0, info: info, retain: nil, release: nil, copyDescription: nil)
	    self.runLoopObserver = CFRunLoopObserverCreate(kCFAllocatorDefault, CFRunLoopActivity.allActivities.rawValue, true, 0, runLoopCallBack(), &context)
	    
2. 然后将这个观察对象添加到runloop的common modes中

		CFRunLoopAddObserver(CFRunLoopGetCurrent(), self.runLoopObserver, CFRunLoopMode.commonModes)
		
	ps: 因为common modes是会一直存在于runloop中的，不会被中断，所以讲检测的observer对象放到这个modes里去。
	
3. 检测CFRunLoopActivity

	CFRunLoopActivity这个结构有非常多的状态吧，我们需要判断的是:
	
		beforeSources: 进入睡眠前
        afterWaiting: 唤醒后的状态
        
   如果runloop返回的activity的值是上述的两个，那么就可以认为出现了卡顿的现象
   
4. 这里用了dispatch的信号机制

	self.dispatchSemaphore?.wait(timeout: DispatchTime.now() + 1 / 50)
	
	这段代码认定，如果每秒的帧数少于50，那么就认为发生了卡顿的现象
	
实现的逻辑就是这么四步，下面贴上全部的代码:

	import Foundation

	class Monitor {
	  
	  static let shared = Monitor()
	  
	  private var runLoopObserver: CFRunLoopObserver?
	  private var dispatchSemaphore: DispatchSemaphore?
	  private var runLoopActivity: CFRunLoopActivity?
	  
	  init() {}
	  
	  func beginMonitor() {
	    guard self.runLoopObserver == nil else { return }
	    
	    self.dispatchSemaphore = DispatchSemaphore(value: 0)
	
	    let info = Unmanaged<Monitor>.passUnretained(self).toOpaque()
	    var context: CFRunLoopObserverContext = CFRunLoopObserverContext(version: 0, info: info, retain: nil, release: nil, copyDescription: nil)
	    self.runLoopObserver = CFRunLoopObserverCreate(kCFAllocatorDefault, CFRunLoopActivity.allActivities.rawValue, true, 0, runLoopCallBack(), &context)
	    
	    CFRunLoopAddObserver(CFRunLoopGetCurrent(), self.runLoopObserver, CFRunLoopMode.commonModes)
	    
	    DispatchQueue.global().async {
	      // 如果少于50每帧, 则认为卡顿
	      while true {
	        guard let sem = self.dispatchSemaphore?.wait(timeout: DispatchTime.now() + 1 / 50) else { return }
	        if case DispatchTimeoutResult.timedOut = sem {
	          guard let _ = self.runLoopObserver else {
	            self.dispatchSemaphore = nil
	            self.runLoopActivity = nil
	            return
	          }
	          
	          // beforeSources: 进入睡眠前
	          // afterWaiting: 唤醒后的状态
	          if (self.runLoopActivity == CFRunLoopActivity.beforeSources || self.runLoopActivity == CFRunLoopActivity.afterWaiting) {
	            print("symbo: \(Thread.callStackSymbols)")
	            print("打印卡顿堆栈...")
	          }
	        }
	      }
	    }
	  }
	  
	  func endMonitor() {
	    if self.runLoopObserver != nil {
	      return
	    }
	    
	    CFRunLoopRemoveObserver(CFRunLoopGetCurrent(), self.runLoopObserver, CFRunLoopMode.commonModes)
	    self.runLoopObserver = nil
	  }
	  
	}
	
	extension Monitor {
	  func runLoopCallBack() -> CFRunLoopObserverCallBack {
	    return { (observer, activity, context) -> Void in
	      let weakSelf = Unmanaged<Monitor>.fromOpaque(context!).takeUnretainedValue()
	      weakSelf.runLoopActivity = activity
	      weakSelf.dispatchSemaphore?.signal()
	    }
	  }
	}
