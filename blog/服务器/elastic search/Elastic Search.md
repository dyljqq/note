# Elastic Search

### 简介

Elasticsearch 是一个高度可扩展且开源的全文检索和分析引擎。它可以让您快速且近实时地存储，检索以及分析海量数据。它通常用作那些具有复杂搜索功能和需求的应用的底层引擎或者技术。

#### 基础概念

* Near Realtime(近实时)
* Cluster(集群)
* Node(节点)
* index(索引)
* Type(类型)
* Document(文档)
* Shards & Replicas(分片 & 副本)

#### 如何通信???

首先需要知道的是，elastic search提供了一个非常全面和强大的REST API(Representation State Transfer API), 我们可以通过这些API完成以下的操作:

 * 检查集群，节点，和索引健康，状态和统计信息
 * 管理集群，节点，索引数据和元数据
 * 针对索引执行CRUD和搜索操作
 * 执行高级搜索，如sorting，filtering等

 1. 集群健康

 		curl -XGET 'localhost:9200/_cat/health?v&pretty'
 		
 	结果:
 		
 	epoch      timestamp cluster                 status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
 	
	1545637330 15:42:10  es-cn-4590s4d0m0005rtl2 green           2         2     42  21    0    0        0             0                  -                100.0%
	

	status的三种状态:
		
	1) green: 表示一切正常
	
	2) yellow: 表示所有数据可用，但是有些副本尚未分配
		
	3) red: 由于某些原因，有些数据不可用
	
	从上面我们可以看出这个集群一共有2个node，42个分片。
	
2. 获取节点列表

		GET /_cat/nodes?v
	
	结果:
		
		ip           heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
		
		172.16.210.8           49          87   6    0.01    0.04     0.05 mdi       -      00iH6O8

		172.16.210.7           33          90  14    0.39    0.23     0.12 mdi       *      tHUn9u-
		
		参数的含义:
		heap.percaentage: Used heap percentage
		ram.percentage: Used total memory
		cpu: Recent system CPU usage as percent
		load_1m: Most recent load average
		load_5m: Load average for the last five minutes
		load_15m: Load average for the last fifteen minutes
		
3. 获取所有的索引

		health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size

		green  open   coupon                          Cf13B_sFTGaRtsFQxCL-AA   5   1    1553479       300506      2.2gb          1.1gb
		
4. 创建一个索引

		PUT /lukou?pretty
		
		结果:
		{u'index': u'lukou', u'acknowledged': True, u'shards_acknowledged': True}
		
5. Index and Query a Document

		POST lukou/lukou/1?pretty -d
		{
			'name': 'jqq'
		}
		
		GET lukou/lukou/1?pretty
		{
		  	'_type': u'lukou',
		  	'_source': {
		  		'name': u'jqq_350227'
			},
			'_index': u'lukou',
			'_version': 1,
			'found': True,
			'_id': u'1'
		}
		
		返回了这个文档在elastic search中的信息。
		
6. 批量处理

		{
		  "took" : 19,
		  "errors" : false,
		  "items" : [
		    {
		      "index" : {
		        "_index" : "lukou",
		        "_type" : "lukou",
		        "_id" : "1",
		        "_version" : 1,
		        "result" : "created",
		        "_shards" : {
		          "total" : 2,
		          "successful" : 2,
		          "failed" : 0
		        },
		        "_seq_no" : 0,
		        "_primary_term" : 1,
		        "status" : 201
		      }
		    },
		    {
		      "index" : {
		        "_index" : "lukou",
		        "_type" : "lukou",
		        "_id" : "2",
		        "_version" : 1,
		        "result" : "created",
		        "_shards" : {
		          "total" : 2,
		          "successful" : 2,
		          "failed" : 0
		        },
		        "_seq_no" : 0,
		        "_primary_term" : 1,
		        "status" : 201
		      }
		    }
		  ]
		}
		
### 执行搜索

首先介绍一下搜索语法，如下所示:

	搜索语句:
	{
		'query': {'match_all': {}},
		'from': 0,
		'size': 10
	}
	
	字段名称:
	query: 查询条件
	from: 搜索结果的开始位置
	to: 搜索结果返回的条数
	
	执行结果:
	{
	  u'hits': {
	  u'hits': [
	  {
	  u'sort': [
	  63.92121],
	  u'_type': u'commodity',
	  u'_source': {
	  u'category': u'',
	  u'sort_score': 63.92121124240725,
	  u'update_time': u'2018-12-21T20:45:19Z',
	  u'has_coupon': 0,
	  u'title': u'\u725b\u4ed4\u88e4\u5973\u88e4\u79cb\u51ac\u5b632018\u65b0\u6b3e\u5916\u7a7f\u663e\u7626\u7f51\u7ea2\u52a0\u539a\u957f\u88e4\u7d27\u8eab\u5c0f\u811a\u9ad8\u8170\u52a0\u7ed2',
	  u'is_del': 0,
	  u'price': 36.9,
	  u'taobao_cids': [
	  162205,
	  16],
	  u'category_ids': [
	  1689,
	  1693,
	  1698],
	  u'content': u'\u4eca\u65e5\u65b0\u54c1\u5c1d\u9c9c\u7279\u4ef729.9\u5143 \u9650\u8d2d\u4e24\u6761 \u4e0d\u503c\u9000\u5168',
	  u'source': 100,
	  u'last_selected_time': u'2018-08-26T07:01:25Z',
	  u'shop_id': 102176025,
	  u'commission': 5.5,
	  u'coupon_price': 0,
	  u'sale_num': 394362,
	  u'id': u'3392796'
	},
	u'_score': None,
	u'_index': u'coupon',
	u'_id': u'3392796'
	},
	{
	  u'sort': [
	  63.63122],
	  u'_type': u'commodity',
	  u'_source': {
	  u'category': u'',
	  u'sort_score': 63.63122172146292,
	  u'update_time': u'2018-12-21T16:37:31Z',
	  u'has_coupon': 1,
	  u'title': u'\u79cb\u51ac\u5b63\u8fd0\u52a8\u88e4\u7537\u58eb\u4f11\u95f2\u88e4\u52a0\u7ed2\u52a0\u539a\u5bbd\u677e\u88e4\u5b50\u7537\u97e9\u7248\u6f6e\u6d41\u675f\u811a\u88e4\u54c8\u4f26\u88e4',
	  u'is_del': 0,
	  u'price': 58.0,
	  u'taobao_cids': [
	  3035,
	  30],
	  u'category_ids': [
	  1699,
	  1703,
	  1872],
	  u'content': u'',
	  u'source': 1,
	  u'last_selected_time': u'2018-08-17T23:04:59Z',
	  u'shop_id': 436868244,
	  u'commission': 20.0,
	  u'coupon_price': 10.0,
	  u'sale_num': 366690,
	  u'id': u'3325953'
	},
	u'_score': None,
	u'_index': u'coupon',
	u'_id': u'3325953'
	}],
	u'total': 1553479,
	u'max_score': None
	},
	u'_shards': {
	  u'successful': 5,
	  u'failed': 0,
	  u'skipped': 0,
	  u'total': 5
	},
	u'took': 116,
	u'timed_out': False
	}

	
	参数介绍:
	* took: 搜索花费的时间
	* time_out: 搜索是否超时
	* _shards: 搜索了几个分片
	* hits: 搜索结果
	* hits.total: 满足搜索条件的文档数目,这里是1553479个
	* hits.hits: 满足条件的数组
	* sort: 结果的排序Key值，没有指定的话就默认按照score排序

搜索中，过滤的语法如下:

	data = {
            'query': {
                'bool': {
                    'must': {'match_all': {}},
                    'filter': {
                        'range': {
                            'price': {
                                'gte': 2000,
                                'lte': 9999
                            }
                        }
                    }
                }
            },
            '_source': ['price', 'title'],
            'sort': {'sort_score': {'order': 'desc'}},
            'size': 2
        }
	
	这个意思是找到文档中，满足价格在2000~9999的商品，我们商品库里会有这么贵的商品么，显然是有的啊。让你们感受下，会是什么样的商品呢:
	
	{
	  u'hits': {
	  u'hits': [
	  {
	  u'sort': [
	  4.2664695],
	  u'_type': u'commodity',
	  u'_source': {
	  u'price': 2548.0,
	  u'title': u'波司登中长款羽绒服男士冬季厚外套漫威系列2018新款B80142527DDS'
	},
	u'_score': None,
	u'_index': u'coupon',
	u'_id': u'4245808'
	},
	{
	  u'sort': [
	  3.1328213],
	  u'_type': u'commodity',
	  u'_source': {
	  u'price': 2808.0,
	  u'title': u'敦奴羊剪绒大衣2018冬季新款中长款连帽系带收腰羊毛外套'
	},
	u'_score': None,
	u'_index': u'coupon',
	u'_id': u'4841820'
	}],
	u'total': 3102,
	u'max_score': None
	},
	u'_shards': {
	  u'successful': 5,
	  u'failed': 0,
	  u'skipped': 0,
	  u'total': 5
	},
	u'took': 74,
	u'timed_out': False
	}
	
### 总结
好了，到这里，elastic search的介绍就结束了。在我们的实际的使用中，用到的其实也就是上面介绍的一些知识点，无非是需要写一些稍微复杂一点的查询语句等等，因为后台搜索需要的条件比较多，比如需要满足一些特定的分类，需要价格区间，优惠券价格区间等等，但是只要掌握它的一些规则，这些其实还是很简单的。有兴趣的朋友可以一起讨论一下。其实elastic search还有很多很高级的东西，在我的实践中并没有涉及，我也只是粗粗的看了一些，比如一些关键词的映射啊，比如如何做一些特定的分词等等，比如如何做一些查询的优化啊，这些都是后面会去探索的东西，并看看能否应用在我们伟大的熊猫优选上面。

		
	
	
 		