# IBInspectable & IBDesignable #

 Xcode6之后给我提供了两种新的装饰器，来展示所见即所得。
 
 1. IBInspectable
 	
	虽然很早之前就知道有这么一个属性了，但是一直都没怎么用过。原因是之前一直都是手写布局，所以这些装饰对我本身而言其实是很鸡肋的。但现在大量的开始用xib进行布局，经常有碰见某个视图需要有圆角的属性，总是要去代码里设置，就特别的不爽。因为你还要每次都去看看效果咋样。
 	
 	所以这个关于圆角的扩展就深得我心。
	
		extension UIView {
			@IBInspectable var cornerRadius: CGFloat {
				get {
					return layer.cornerRadius
				}
				set {
					layer.cornerRadius = newValue
					layer.masksToBounds = newValue > 0
				}
			}
		}
		
		
2. IBDesignable
	
	这个装饰器的话，用在UIView中的话，可以让自定义的视图在更改的时候，就渲染出视图来。使用如下:
	
		@IBDesignable
		class MyCustomView: UIView {
			// TODO
		}
		
		
### 下面插播一条小集

Why should we implements this initializer:

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)	
	}
	


Reasons:	

I'll start this answer from the opposite direction: what if you want to save state of your view to disk? This is a know as serialization. The reverse is deserialization - restoring the state of the object from disk.
	
The NSCoding protocol defines 2 methods to serialize and deserialize:

	func encoderWithCoder(_ aCoder: NSCoder) {
		// Serialize your object here
	}
	
	func init(coder aDecoder: NSCoder) {
		// Deserialize your object here
	}
	
So why is it needed in your custom class? The answer is Interface Builder. When you drag an object onto a storyboard and configure it, Interface Builder serializes the state of that object on to disk, then deserialize it when the storyboard appears on screen. You need to tell Interface Builder how to do those. At the very least, if you don't add any new properties to your subclass, you can simply ask the superclass to do the packing and unpacking for you, hence the super.init(coder: aDecoder) call. If your subclass is more complex, you need to add your own serialization and deserialization code for the subclass.

This is in contrast to the Visual Studio's approach, which is to write code into a hidden file to make the object at run time.