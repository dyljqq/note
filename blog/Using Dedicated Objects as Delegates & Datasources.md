# 给UITableView写一个适配器

### 前言

我们在构建一个包含UITableView的UIViewController的时候，总是会写如下的代码:

	tableView.delegate = self
	tableView.dataSource = self
	
然后再实现我们需要的一些tableView的委托方法。但是很多时候，这些方法都是重复的，主要的区别就是，dataSource的model不一样。逻辑其实都是相同的，所以，我们可以抽象出一个Adapter，来专门写这些逻辑。

### 具体的代码

	class ListDataSource<T>: NSObject, UITableViewDataSource, UITableViewDelegate {
	  
	  fileprivate let items: [T]
	  
	  let cellFactory: (T) -> (UITableViewCell)
	  let cellHeightClosure: ((T) -> (CGFloat))?
	  
	  var scrollViewDidScrollClosure: ((UIScrollView) -> ())?
	  
	  init(items: [T], cellFactory: @escaping (T) -> (UITableViewCell), cellHeightClosure: ((T) -> (CGFloat))? = nil) {
	    self.items = items
	    self.cellFactory = cellFactory
	    self.cellHeightClosure = cellHeightClosure
	  }
	  
	  func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
	    return items.count
	  }
	  
	  func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
	    return self.cellFactory(items[indexPath.row])
	  }
	  
	  func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
	    guard let closure = self.cellHeightClosure else {
	      return 44.0
	    }
	    return closure(items[indexPath.row])
	  }
	  
	  func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
	    tableView.deselectRow(at: indexPath, animated: true)
	  }
	  
	  func scrollViewDidScroll(_ scrollView: UIScrollView) {
	    if let closure = scrollViewDidScrollClosure {
	      closure(scrollView)
	    }
	  }
	}
	
然后实例化它，如下:

	fileprivate var currentDataSource: (UITableViewDataSource & UITableViewDelegate)? {
	    didSet {
	      tableView.delegate = currentDataSource
	      tableView.dataSource = currentDataSource
	      tableView.reloadData()
	    }
  	}
	
	func setDataSource() {
	    let cellFactory: (CellDataType) -> (UITableViewCell) = { [unowned self] type in
	      switch type {
	      case .title(let title):
	        let cell = self.tableView.dequeue() as TitleCell
	        cell.render(text: title)
	        return cell
	      case .story(let story):
	        let cell = self.tableView.dequeue() as StoryCell
	        cell.render(story: story)
	        return cell
	      }
	    }
	    let cellHeightClosure: (CellDataType) -> (CGFloat) = { type in
	      return type.height
	    }
	    let dataSource = ListDataSource<CellDataType>(items: self.dataSource, cellFactory: cellFactory, cellHeightClosure: cellHeightClosure)
	    dataSource.scrollViewDidScrollClosure = { [unowned self] scrollView in
	      self.setupNavigationBar(by: scrollView.contentOffset.y)
	    }
	    currentDataSource = dataSource
	  }
	  
当然，这是个比较复杂的例子了，大部分时候，我们其实都只是实现一些很简单的逻辑。对于一些复杂的例子，我们完全可以给它们单独定义一个Adapter，而对于简单的来说，就可以用泛型，来重用这个ListDataSource。

### 注意的点:
	
> One tricky thing however when you put your dataSource in a dedicated, separate object, is to not forget to retain it.

> The dataSource property on UITableView is weak (as all dataSources and delegates should be), so if you just affect tableView.dataSource to a newly created ListDataSource(…) without retaining it, that ListDataSource instance will then be released from memory and your UITableView will go back to being empty.

> So when you use that trick, just don’t forget to retain your object serving as DataSource. In the example above, I made the DemoViewController retain it by using a var currentDataSource property, and used that occasion to use a didSet on it to propagate it to the tableView and reload it afterwards.

简单的翻译一下，就是因为UITableView里的dataSource是一个弱变量，所以如果我们给他赋上一个新创建的变量而没有持有它，那么这个变量就会被释放，然后UITableView就会为空。因此我们需要在didSet中给它赋值。

