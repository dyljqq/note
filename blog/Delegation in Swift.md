#Swift中的委托模式

[原文链接](https://www.swiftbysundell.com/posts/delegation-in-swift)

委托模式在苹果的平台中起着很大的作用已经很久了。通过使用UITableViewDelegate来处理TableView的所有响应事件，使用NSCacheDelegate来修改Cache的行为。委托模式的核心目的就是采用解耦的方式，允许该对象跟上一层的持有者进行对话。因为不需要该对象知道它的持有者的具体类型，
所以我们可以更容易的写出易于复用和可维护的代码。

就像我们在[前两篇文章](https://www.swiftbysundell.com/posts/observers-in-swift-part-1)看到的观察者模式一样, 委托者模式可以用许多不同的方法去实现。本周，我们就来看看其中的一些方法，以及它们的优缺点。

###什么时候该使用委托

将某些决策和行为委托给类型拥有者的主要好处是，在支持多个不同的使用实例上，它会变得更加的容易，而不需要创建一个复杂的类型去满足所有的情况。

就拿UITableView和UICollectionView举例。这两个在决定如何渲染的方面，都是极其的灵活的。使用委托者模式，我们可以极其简单的处理交互事件，决定cell该如何创建以及调整它们的排布属性-所有的这些，都不需要任何类去了解它们的具体逻辑。

当一个类型需要在不同的上下文中可用，并且在所有的上下文中都有一个明确的拥有者的时候，委托模式通常都会是一个比较好的方法。就像一个UITableView经常所属与一个父的视图，或者一个视图控制器。和观察者模式相反，使用委托者模式的类型，有且只有一个拥有者，它们是一对一的关系。

###协议

在苹果自己的API中发现的最常见的委托方式就是使用委托协议。就像UITableView有的UITableViewDelegate协议，我们也可以用相似的方式去实现自己的协议。就像下面的为FileImporter类设计的FileImportDelegate协议：

	protocol FileImporterDelegate: AnyObject {
    	func fileImporter(_ importer: FileImporter,
                      shouldImportFile file: File) -> Bool

    	func fileImporter(_ importer: FileImporter,
	                      didAbortWithError error: Error)
	
	    func fileImporterDidFinish(_ importer: FileImporter)
	}
	
	class FileImporter {
	    weak var delegate: FileImporterDelegate?
	}
	
当我们实现自己的委托者协议的时候，尝试遵循苹果自己所建立的命名规范通常会是一个好主意。下面是我们需要谨记的指导方针:

	1. 使方法名可以明确的看出就是委托的方法名，通常我们会在方法名的开头使用委托的类型名。像上面的委托，所有的方法名都以fileImporter开头。
	2. 委托方法的第一个参数通常都是委托对象自己本身。这使得拥有多个实例的对象在处理事件的时候可以轻松的区分开来。
	3. 当使用委托的时候，不要把任何细节泄露给委托人。举个例子，当处理按钮点击事件的时候，把按钮传递给委托方法似乎是非常有用的。但是如果这个按钮是一个私有的视图，那么它就不应该从属与公有的方法。

采用基于协议的路由的优点在于，它是所有的Swift开发者所熟悉的。它也可以将所有的事件方法都分组到一个协议中去，并且如果实现方式不正确，编译器将会报错。

然而，这种方法也有一些缺陷。我们上面的FileImporter示例中最明显的一点是，使用委托协议可能是模糊状态的来源。注意我们该如何委派决定是否应该把给定的文件给委托人。但是如果这个委托是可选的，那么它将变得非常的棘手，当这个委托为空的时候，我们无法决定该怎么处理。

	class FileImporter {
	    weak var delegate: FileImporterDelegate?
	
	    private func processFileIfNeeded(_ file: File) {
	        guard let delegate = delegate else {
	            // Uhm.... what to do here?
	            return
	        }
	
	        let shouldImport = delegate.fileImporter(self, shouldImportFile: file)
	
	        guard shouldImport else {
	            return
	        }
	
	        process(file)
	    }
	}
	
上面的问题我们可以采用多种方式去处理。比如当解包失败的时候，在else的分支中添加assertionFailure()，或者使用默认值。但任何一种处理方式都说明这种设置是存在缺陷的，因为我们正在介绍另一种经典的这种不应该发生的情景，应该避免这种情况。

###闭包

有一种办法可以使上面的代码更可预测，就是在重构的时候，将部分的委托方法用闭包来替代。这样的话，我们的API使用者将被要求决定哪些文件会被预先导入进来的逻辑，然后把这些逻辑从委托中移除：
	
	class FileImporter {
	    weak var delegate: FileImporterDelegate?
	    private let predicate: (File) -> Bool
	
	    init(predicate: @escaping (File) -> Bool) {
	        self.predicate = predicate
	    }
	
	    private func processFileIfNeeded(_ file: File) {
	        let shouldImport = predicate(file)
	
	        guard shouldImport else {
	            return
	        }
	
	        process(file)
	    }
	}
	
随着上述的变化，我们可以继续，然后把shouldImportFile方法从我们的委托协议中删除，只剩下哪些监听状态变化的方法。

	protocol FileImporterDelegate: AnyObject {
	    func fileImporter(_ importer: FileImporter,
	                      didAbortWithError error: Error)
	
	    func fileImporterDidFinish(_ importer: FileImporter)
	}
	
上述的主要优点就是，错误使用FileImporter类将会变得更加的困难。我们现在可以完全正确的去使用它，甚至不需要分配给委托。在这种情况下可能会有用，假如某些文件应该在后台导入，而我们对操作的结果并不感兴趣。

###类型配置

接着说，我们将会继续将剩余的委托方法转化为闭包。一种方法是我们将会简单的将闭包作为初始化的参数或者可变变量添加。然而，如果这么做，我们的API将会变得臃肿。而且，这样我们会更难区分配置选项和其他变量的区别。

一种解决这个困境的方法是使用一个特定的配置类型。这样的话，我们可以实现跟委托协议一样好的事件分组,同时在实现各种事件的时候，仍然后很大的自由度。我们将会采用结构体来定义配置类型，然后给每个事件定义一个属性，如下：
	
	struct FileImporterConfiguration {
	    var predicate: (File) -> Bool
	    var errorHandler: (Error) -> Void
	    var completionHandler: () -> Void
	}
	
我们现在就可以更新FileImporter，使它只拥有一个简单的参数。当初始化这个配置参数的时候，通过将配置项当做属性，我们可以轻松的访问各个闭包:

	class FileImporter {
	    private let configuration: FileImporterConfiguration
	
	    init(configuration: FileImporterConfiguration) {
	        self.configuration = configuration
	    }
	
	    private func processFileIfNeeded(_ file: File) {
	        let shouldImport = configuration.predicate(file)
	
	        guard shouldImport else {
	            return
	        }
	
	        process(file)
	    }
	
	    private func handle(_ error: Error) {
	        configuration.errorHandler(error)
	    }
	
	    private func importDidFinish() {
	        configuration.completionHandler()
	    }
	}
	
使用上述的委托方法，我们也可以实现不错的效果。为各种相同的FileImporter配置项定义便利的API也更加的简单。举个例子，我们可以在FileImportConfiguration添加一个便利的只有predicate一个参数的初始化方法，可以更加容易的去创建一个importer。

	extension FileImporterConfiguration {
	    init(predicate: @escaping (File) -> Bool) {
	        self.predicate = predicate
	        errorHandler = { _ in }
	        completionHandler = {}
	    }
	}
	
作为一个快速的附注：在扩展中添加一个便利的初始化方法，而不是在类型本身定义，是因为这样我们可以继续使用编译器生成的初始化方法。

我们甚至可以创建一个静态的便捷的不需要任何参数的公共配置项，举个例子，一个简单的引入所有文件的变量如下：

	extension FileImporterConfiguration {
	    static var importAll: FileImporterConfiguration {
	        return .init { _ in true }
	    }
	}
	
然后我们可以使用Swift的炫酷的点语法，从而创建一个更加易于使用的API，并且可以一直提供大量的自定义和灵活性：

	let importer = FileImporter(configuration: .importAll)

酷毙了！

###结论

委托者模式将会继续成为苹果的框架和我们的代码库中不可或缺的一部分。但是即使它是一个古老和简单的概念，我们仍然可以使用不同的方法去实现它-每种方法都有它的优缺点。

使用委托协议将会提供一种熟悉和坚实的模式，对于大多数的使用例子来说，它都是一种好的默认实现。使用闭包可有增加更多的灵活性，但是同时也会导致更加复杂的代码（这里不是指会出现循环引用）。配置类型可以提供一个友好的中间地带，但是需要更多的代码（虽然，就像我们所看到的，添加正确的便捷的API，我们的代码可以变得简单很多）。

Thank you for reading。