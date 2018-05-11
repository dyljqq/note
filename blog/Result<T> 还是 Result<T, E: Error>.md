#Result\<T\> Or Result\<T, E: Error\>

[原文链接](https://xiaozhuanlan.com/topic/4718350296)

### 举个例子

	URLSession.shared.dataTask(with: request) {
	    data, response, error in
	        if error != nil {
	            handle(error: error!)
	        } else {
	            handle(data: data!)
	        }
	}
	
URLSession中出现了三个参数，分别是（data, response, error），虽然没有什么大的问题，但是还是可以有一些改进的空间。比如，data和error只可能存在一个为空的情况。因此就会出现对nil的错误解包的情况。那么解决办法呢，当然是有的，就是用Result。

	enum Result<T, E: Error> {
	    case success(T)
	    case failure(E)
	}
	
在Alamofire中，定义的enum其实是:
	
	enum Result<T> {
	    case success(T)
	    case failure(Error)s
	}
	
主要的不同是，第二个情况，我们无法知道具体的错误类型。好了，言归正传，那么如何通过Result去对上面的代码做改造呢，如下：

	extension URLSession {
	    func dataTask(with request: URLRequest, completionHandler: @escaping (Result<(Data, URLResponse), NSError>) -> Void) -> URLSessionDataTask {
	        return dataTask(with: request) { data, response, error in
	            if error != nil {
	                completionHandler(.failure(error! as NSError))
	            } else {
	                completionHandler(.success((data!, response!)))
	            }
	        }
	    }
	}
	
	URLSession.shared.dataTask(with: request) { result in
	    switch result {
	    case .success(let (data, _)):
	        handle(data: data)
	    case .failure(let error):
	        handle(error: error)
	    }
	}
	
这样就可以避免产生可选值为空的情况，在编译器的层面上就避免了因为解包而出现的crash。

###如何使用在我们的项目中

在我们的APIClient中是不是也可以使用这样的方式，来使的代码更加的可维护和健壮呢。

for example:

	enum APIClientResult<T> {
	  case success(T)
	  case failure(String)
	}
	
	使用:
	
	@discardableResult
	  public static func get<Model: Mappable>(path: String, params:[String : AnyObject] = [:],
	                                          completion: @escaping (APIClientResult<Model>) -> Void) -> DataRequest {
	    return request(path, method: .get, params: params) { (model: Model?, _: [Model]?, errorMsg: String?) in
	      if let errorMsg = errorMsg {
	        completion(.failure(errorMsg))
	      } else if let model = model {
	        completion(.success(model))
	      }
	    }
	  }
	  
这当然只是项目中的一个可以考虑使用这个方法改进的地方。但显然这样写出来的代码会更加的健壮一些。