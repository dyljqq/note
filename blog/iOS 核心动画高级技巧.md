# iOS核心动画高级技巧

### Z坐标轴

1. 可以通过z坐标调整sublayer的前后位置, 视图的显示，遵循画家算法.
	
		self.greenView.layer.zPosition = 1.0f
		
	因为浮点数的问题，所以最好取整会好一些。
	
	
2. hit testing
	
	hitTest方法可以用来替代containsPoint, 判断被点击的图层
	
		override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
    	super.touchesBegan(touches, with: event)
    	
    		let point = touches.first!.location(in: self.view)
    		let layer = view.layer.hitTest(point)
    		if layer == view.layer {
      			// TODO
    		}
  		}
  		
  		
  		
3. 图层的呈现与模型
	
	presentationLayer表示的当前屏幕上真正显示的layer。如： 在iOS中，屏幕每秒钟重绘60次。如果动画时长比60分之一秒要长，Core Animation就需要在设置一次新值和新值生效之间，对屏幕上的图层进行重新组织。这意味着CALayer除了“真实”值（就是你设置的值）之外，必须要知道当前显示在屏幕上的属性值的记录。