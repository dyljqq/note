### iOS 13新特性

1. view controller present

	iOS 13之后，present的modalPresentationStyle方式变成了automatic, 呈现的方式并不是全屏显示，而是会顶部留白，默认下拉可以dismiss。
	
	如果想要全屏显示可以如下:
	
		vc.modalPresentationStyle = .fullScreen
		self.present(vc, animated: true)
		
2. 禁用暗黑模式

	将info.plist的UserInterfaceStyle的value设置为light
	
3. iOS 13中禁用KVC调用私有属性

	比如:
	
		let searchField: UITextField = self.searchBar.value(forKey: "")
	   	let placeHolderLabel: UILabel = searchField.value(forKey: "placeHolderLabel")
	    placeHolderLabel.textColor = UIColor.red
		
	上面这个会引起crash，正确的做法：
	
		let textField = self.searchBar.searchTextField // in iOS 13
		let attr = NSMutableAttributedString(string: "aaaa")
    	textField?.attributedPlaceholder = attr
    	
4. keyWindow

	iOS 13为了适配多屛，如果是多屏的应用的话，那么:
	
		UIApplication.shared.keyWindow 
		
	就不应该再被使用
	
		@available(iOS, introduced: 2.0, deprecated: 13.0, message: "Should not be used for applications that support multiple scenes as it returns a key window across all connected scenes")
    	open var keyWindow: UIWindow? { get }
    	
    取而代之的应该是:
    
    	UIApplication.shared.windows.filter { $0.isKeyWindow }.first