# elastic search打分机制

Lucene采用实用评分函数的公式来计算相关度。包含了词频/逆向文档频率， 向量空间模型，还有一些协调因子，字段长度归一化。

### 词频/逆向文档频率(TF/IDF)

1. 词频

	词频是指一个词在文档中出现的频率是多少。比如hello world这个查询短句， 分别统计出hello与world在某个文档中，出现的次数的平方根就是词频:
	
		tf = sqrt(frequency)
		
2. 逆向文档频率

	上面的计算有些问题，那就是有些词在所有的文档中，都出现的非常频繁，那么这些词的频次越高，权重越低：
	
		idf = 1 + log(numDocs / (docFreq + 1))
		
### 字段归一值

字段的长度越短，字段的权重越高。

	norm(d) = 1 + sqrt(numTerms)
	
### 向量空间模型

向量空间模型中的每个数字都代表一个词的权重，那么我们就能根据这个数组，构建一个向量。然后我们可以比较一个文档与这个向量的余弦值，来判断相关性。

### 计算score

	score(q, d) = queryNorm(q) * coord(q, d) * sum(tf(t in d) * idf(t)^2 * t.getBoost() * norm(t, d))(t in  q)

* queryNorm(q): 查询归一化因子
* coord(q, d): 协调因子
* t.getBoost(): 查询中使用的boost

t.getBoost()，我们可以通过修改这个值，来修改到各个查询的权重。正相关。


