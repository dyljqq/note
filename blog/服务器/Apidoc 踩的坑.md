# 在安装Apidoc中我踩的坑

[Apidoc github 地址](https://github.com/apidoc/apidoc)

首先按照网上的教程，安装apidoc的步骤只有这么几步:

	brew install node  // (如果没有安装过node的话)
	sudo npm install apidoc -g // 然后安装全局的apidoc
	
可是我安装完后，使用apidoc的指令，没用啊。报的错误都是：

	zsh not found apidoc command
	
就是我识别不出来啊，你安装了也没安装。而且奇怪的是，大家好像都是一遍就安装通过的。所以呢，这里我记录一下，我是怎么安装的呢。

首先进入到根目录，然后执行:

	npm install apidoc

这个时候，根目录下就会有一个node初始化完的所有文件，其实这样不好啊，但是，emmmm。然后你会看到有node_modules的文件夹。然后cd到apidoc，将bin目录下的apidoc指令，软连接到/usr/local/bin下就可以了！

最后执行:

	apidoc -i {source category} -o apidoc/
	
前提是你已经写了apidoc.json文件了，里面是一些生成文档的配置信息。

至于怎么写这个api doc, 那就自行google。