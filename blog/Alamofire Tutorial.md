# Alamofire教程

![](https://koenig-media.raywenderlich.com/uploads/2016/12/Alamofire-feature-250x250.png)

Alamofire是一个为iOS和Mac设计的基于swift的HTTP网络库。它在Apple的基础框架上，提供了一个优雅的接口，简化了一些公共的网络任务。

Alamofire提供了链式的请求/响应方法，JSON参数以及响应的序列化，认证，和更多的其他特性。在这篇Alamofire的教程中，你将会使用Alamofire去实现一个基础的网络任务，比如上传文件，从第三方的RESTful API请求数据。

Alamofire的优雅来自于它是用swift重新写过的，并没有任何继承于它的Object-C版本，叫做AFNetworking。

你应该对HTTP和苹果提供的一些我们可以查看的网络类，像URLSession，有一些基本的了解。

虽然Alamofire有一些实现的细节有些模糊，但是如果你有一些如何解决你的网络请求的背景知识的话，它将是有益的。你也会需要安装CocoaPods，然后通过它将Alamofire安装到你的项目中去。


## 开始

下载[初始项目]("https://koenig-media.raywenderlich.com/uploads/2016/12/PhotoTagger-starter-1.zip")

这个基于Alamofire的App名叫PhotoTagger。当这个项目完成的时候，它将会让你从你的相册中选择一张照片（如果是在真正的设备中启动这个app的话，你可以拍照），然后将这张照片上传到第三方的服务网站上，这个网站将会做一些图片识别的任务，然后返回一系列的图片标志和一些初始的颜色。

![](https://koenig-media.raywenderlich.com/uploads/2015/11/PhotoTaggerDemo.gif)

编译并且运行这个项目，你将会看到下面的效果：

![](https://koenig-media.raywenderlich.com/uploads/2015/11/PhotoTagger-start.png)

点击Select Photo按钮，并且选择一张图片。背景图将会变成你选择的图片。

打开Main.storyboard然后你会看到展示标签和颜色的界面已经给你建好了。剩下的工作只是上传图片，然后获取它的标签和颜色。

## Imagga API

Imagga是一个提供图像处理服务的平台，它会为开发者和公司提供提供图片标签的API，以构建可扩展的图像密集型云应用程序。你可以在[这里]("https://imagga.com/auto-tagging-demo?url=https://imagga.com/static/images/tagging/vegetables.jpg")演示如果自动给图片打标签。

在这个教程中，你需要在Imagg创建一个免费的账号。Imagga需要在HTTP请求的头部加入验证，因此只有注册了他们服务的人可以使用。进入[https://imagga.com/auth/signup/hacker](https://imagga.com/auth/signup/hacker)，然后填写表单。在你创建账户之后，检查你的dashboard:

![](https://koenig-media.raywenderlich.com/uploads/2015/12/Imagga-Dashboard-700x458.png)

在Authorization模块是你的私密token，你将会在接下来使用它。在接下来的所有HTTP请求头部，都需要包含它。

	备注：你要确保你复制了整段的token， 务必滑动到最右边并且复制了所有的内容。
	
你将会使用Imagga的内容端去上传图片，标记图像识别的端点以及颜色识别的端点。你可以在[http://docs.imagga.com](http://docs.imagga.com)看到所有Imagga的API。

## 安装依赖

在项目的主目录下创建一个名为Podfile的文件，然后往里面加入：
	
	platform :ios, '10.0'

	inhibit_all_warnings!
	use_frameworks!

	target 'PhotoTagger' do
 	 pod 'Alamofire', '~> 4.2.0'
	end
	
然后，打开你的终端，输入如下命令:

	pod install
	
如果你的机器上没有安装CocoaPods，查看这篇教程[如何使用CocoaPods](How to Use CocoaPods with Swift tutorial)获取更多信息。

	备注: 确保你安装的是最新的CocoaPods。如果不是的话，你可能会看到很多的编译错误提示。在写篇文章的时候，最新的版本应该是1.1.1。
	
关闭当前的工程，然后打开新创建的PhotoTagger.xcworkspace。编译运行你的工程，在启动的app中，你并不会注意到一些可视的变化。这是非常棒的。接下来的任务就是添加一些网络请求， 从一个RESTFul的服务器上抓取JSON数据。