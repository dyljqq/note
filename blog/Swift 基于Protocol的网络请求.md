# Swift 基于Protocol的网络请求

这次的网络请求的数据来自知乎日报

### 构建一个Router

首先我们用enum来构建一个请求：
	
	enum Router {
  		case lastNews // 获取知乎日报的首页数据
  		case oldStories(String) // 获取以前的story
	}
	
然后将所有的跟Request有关的东西都在Router里配置, Alamofire里有个URLRequestConvertible协议就是做这个的，我们来看下这个协议的定义:
	
	/// Types adopting the `URLRequestConvertible` protocol can be used to construct URL requests.
	public protocol URLRequestConvertible {
    	/// Returns a URL request or throws if an `Error` was encountered.
    	///
    	/// - throws: An `Error` if the underlying `URLRequest` is `nil`.
    	///
    	/// - returns: A URL request.
    	func asURLRequest() throws -> URLRequest
	}
	
然后我们只要实现asURLRequest方法，再配置好对应的HTTPMethod, header， parameter以及完整的URL，如下:
	
	extension Router: URLRequestConvertible {
  
  		static let baseURL = "http://news-at.zhihu.com/api/4/"
  
  		var method: HTTPMethod {
    		return .get
  		}
  
  		var headers: [String: String] {
    		return [:]
  		}
  
  		var parameters: [String: Any] {
    		return [:]
  		}
  
  		var path: String {
    		switch self {
    			case .lastNews: return "news/latest"
    			case .oldStories(let dateString): return "news/before/" + dateString
    		}
  		}
  
  		func asURLRequest() throws -> URLRequest {
    		let url = try Router.baseURL.asURL()
    		var request = URLRequest(url: url.appendingPathComponent(path))
    		request.httpMethod = method.rawValue
    		request.allHTTPHeaderFields = headers
    		request.timeoutInterval = TimeInterval(10 * 1000)
    		return try URLEncoding.default.encode(request, with: parameters)
  		}
  
	}
	
### 设计网络请求

定义一个APIClietable的协议，这个协议默认实现了一个网络请求方法:

	func send<T: Decodable>(router: Router, completionHandler: @escaping (T?) -> ())
	
方法的里面会做下载下来的数据的二次加工，因为请求的数据一般都是JSON格式的，所以我们可以用SwiftJSON的第三方库做数据的解析。

实现如下:
	
	Alamofire.request(router).validate().responseJSON { response in
      switch response.result {
      case .success(let value):
        let json = JSON(value)
        completionHandler(T.parse(data: json))
      case .failure(let error):
        print("Request Error: \(error)")
        completionHandler(nil)
      }
    }
    
但是很显然返回的数据要有一个统一的形式，这样才能方便我们的解析，不然每次都在回调中进行数据的解析，会增加很多无谓的代码。因此我定义了一个解析的协议，所有的Model都需要实现这个协议。

### Decodable

	protocol Decodable {
  		static func parse(data: JSON) -> Self
	}
	
Decodable协议里定义了一个parse的方法，用来对数据进行解析。

### Model

	struct Story {
  
  		let id: Int
  		let title: String
  		let type: Int
  		let image: String
  		let images: [String]
  
  		init(_ json: JSON) {
    		self.id = json["id"].intValue
    		self.title = json["title"].stringValue
    		self.type = json["type"].intValue
    		self.images = json["images"].arrayValue.flatMap { $0.stringValue }
    
    		self.image = self.images.isEmpty ? json["image"].stringValue : (self.images.first ?? "")
  		}
  
	}
	
定义了一个Story的model，用来解析知乎日报里的流数据，如果不实现Decodable协议的话，那么我们就需要特定的Model去承载数据了，这样的话，会也别的麻烦。

	extension Story: Decodable {
  
  		static func parse(data: JSON) -> Story {
    		return Story(data)
  		}
  
	}
	
最后就是使用这个网络请求方法了

	send(router: Router.lastNews, completionHandler: { (storyList: StoryList?) in
      guard let storyList = storyList else { return }
      print("last news: \(storyList)")
    })
    
输出如下:
	
	last news: StoryList(date: "20180330", stories: [ZhihuDailyReport.Story(id: 9676477, title: "「不可能跟老板提加薪的，哪怕我心里已经想得要命」", type: 0, image: "https://pic2.zhimg.com/v2-684fea996c8cb952b480dee552191f2d.jpg", images: ["https://pic2.zhimg.com/v2-684fea996c8cb952b480dee552191f2d.jpg"]), ZhihuDailyReport.Story(id: 9676705, title: "B 站赴美上市后值得投资吗？", type: 0, image: "https://pic2.zhimg.com/v2-557dcc6966e65744be27c3c4b2e35d59.jpg", images: ["https://pic2.zhimg.com/v2-557dcc6966e65744be27c3c4b2e35d59.jpg"]), ZhihuDailyReport.Story(id: 9676615, title: "「最怕去医院了，楼上楼下跑，一折腾就是一天」", type: 0, image: "https://pic2.zhimg.com/v2-d867b7379b445db6c4c78ce8f296ef0d.jpg", images: ["https://pic2.zhimg.com/v2-d867b7379b445db6c4c78ce8f296ef0d.jpg"]), ZhihuDailyReport.Story(id: 9676268, title: "工作时喜欢外放音乐的人，我其实挺佩服你们的", type: 0, image: "https://pic2.zhimg.com/v2-70ad93512f46d460fe45bc93388a4755.jpg", images: ["https://pic2.zhimg.com/v2-70ad93512f46d460fe45bc93388a4755.jpg"]), ZhihuDailyReport.Story(id: 9676651, title: "一直不理解，为什么很多女生对 GAY 有好感？", type: 0, image: "https://pic4.zhimg.com/v2-1984722ad4872e5bbc0211e203f03bcb.jpg", images: ["https://pic4.zhimg.com/v2-1984722ad4872e5bbc0211e203f03bcb.jpg"]), ZhihuDailyReport.Story(id: 9676605, title: "放下你翘着的二郎腿，了解下这个坏习惯会产生的严重后果", type: 0, image: "https://pic4.zhimg.com/v2-7c6f682169570bba5c8c509d72745e4b.jpg", images: ["https://pic4.zhimg.com/v2-7c6f682169570bba5c8c509d72745e4b.jpg"]), ZhihuDailyReport.Story(id: 9676482, title: "大误 · 是时候表演真正的技术了", type: 0, image: "https://pic1.zhimg.com/v2-20745139adcfe1c0075975edb4fd785c.jpg", images: ["https://pic1.zhimg.com/v2-20745139adcfe1c0075975edb4fd785c.jpg"]), ZhihuDailyReport.Story(id: 9676060, title: "故宫的「俏格格娃娃」，都说了是原创，为什么还召回？", type: 0, image: "https://pic2.zhimg.com/v2-1765fba5efa45c7c940a61018e9e482d.jpg", images: ["https://pic2.zhimg.com/v2-1765fba5efa45c7c940a61018e9e482d.jpg"]), ZhihuDailyReport.Story(id: 9675216, title: "阳台适合种哪些可以吃的花？", type: 0, image: "https://pic2.zhimg.com/v2-e8f7698fa3e6628861eac7b8b2e58b89.jpg", images: ["https://pic2.zhimg.com/v2-e8f7698fa3e6628861eac7b8b2e58b89.jpg"]), ZhihuDailyReport.Story(id: 9676419, title: "程序员到了 30 岁，是时候该考虑一些事了", type: 0, image: "https://pic2.zhimg.com/v2-578ac82d0514be6fc40b34f011182391.jpg", images: ["https://pic2.zhimg.com/v2-578ac82d0514be6fc40b34f011182391.jpg"]), ZhihuDailyReport.Story(id: 9676379, title: "婚姻中有哪些人性的黑暗面？", type: 0, image: "https://pic1.zhimg.com/v2-2cbe2bd2271a4a1a4c6938107ab12894.jpg", images: ["https://pic1.zhimg.com/v2-2cbe2bd2271a4a1a4c6938107ab12894.jpg"]), ZhihuDailyReport.Story(id: 9675149, title: "增长、刷屏、砸钱和产品演化：2018，互联网「下半场」", type: 0, image: "https://pic2.zhimg.com/v2-fb8deca37e5d6880c0e2911b33d76881.jpg", images: ["https://pic2.zhimg.com/v2-fb8deca37e5d6880c0e2911b33d76881.jpg"]), ZhihuDailyReport.Story(id: 9676586, title: "瞎扯 · 如何正确地吐槽", type: 0, image: "https://pic1.zhimg.com/v2-02c85840139e14330dd20244024a30ec.jpg", images: ["https://pic1.zhimg.com/v2-02c85840139e14330dd20244024a30ec.jpg"])], topStories: [ZhihuDailyReport.Story(id: 9676615, title: "「最怕去医院了，楼上楼下跑，一折腾就是一天」", type: 0, image: "https://pic4.zhimg.com/v2-9fd3ff91d902500917c65939ea926ec7.jpg", images: []), ZhihuDailyReport.Story(id: 9676268, title: "工作时喜欢外放音乐的人，我其实挺佩服你们的", type: 0, image: "https://pic2.zhimg.com/v2-5b4e1e5bb34f8988e0ac339cc1395289.jpg", images: []), ZhihuDailyReport.Story(id: 9676651, title: "一直不理解，为什么很多女生对 GAY 有好感？", type: 0, image: "https://pic4.zhimg.com/v2-fa7290f20b04123113399469b2dade67.jpg", images: []), ZhihuDailyReport.Story(id: 9676605, title: "放下你翘着的二郎腿，了解下这个坏习惯会产生的严重后果", type: 0, image: "https://pic4.zhimg.com/v2-9141608284a72626361d45e1839a2083.jpg", images: []), ZhihuDailyReport.Story(id: 9676060, title: "故宫的「俏格格娃娃」，都说了是原创，为什么还召回？", type: 0, image: "https://pic4.zhimg.com/v2-a6927b8f2287f32dfa8b3921632b3fe7.jpg", images: [])])
