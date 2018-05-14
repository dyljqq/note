# UIBezierPath for arc

### 初始化方法

	init(arcCenter:radius:startAngle:endAngle:clockwise:)
	
### 参数介绍

1. *center*
	
	在当前的坐标系中，确定圆弧的圆心
	
2. *radius*

	确定圆弧的半径
	
3. *startAngle*

	确定圆弧的起始的角度
	
4. *endAngle*

	确定圆弧的终止角度
	
5. *clockwise*

	画圆角的方向（true为顺时针，而非逆时针）
	
### 返回值

一个特定圆弧的路径对象

### 如何根据参数来确定圆弧

苹果确定圆弧的步骤跟要填写的参数顺序是一样的，即：

1. 先确定圆心
2. 再确定起始点
3. 确定终结点
4. 最后连接这两个点，连接的顺序是根据clockwise来敲定，true为顺时针，false为逆时针。