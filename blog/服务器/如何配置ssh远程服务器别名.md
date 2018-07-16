# 如何配置ssh远程服务器别名

首先，如果我们不采用别名的形式，我们是怎么访问远程的服务器呢，一般是不是:

	ssh root@127.0.0.1
	
然后要求你输入密码，输入正确的密码后，你就能正常的访问这个服务器了。

	ps: 
	1. 其实我们可以通过ssh-keygen命令，来生成本地的公钥
	2. 通过ssh-copy-id将公钥上传到服务器
	这样下次登录的时候，服务器会下发一段随机的文本，本地用私钥加密后，上传给服务器，服务器通过公钥解密，然后比对是否相同。
	
## 设置别名

	1. 进入到.ssh目录中，查看是否有config文件，没有的话，touch config
	2. vim config后，按照以下格式输入对应的信息

	Host hero
	HostName 127.0.0.1
	User root
	identitiesOnly yes
	
	// 以下为注释
	Host: 服务器的别名（自己设置）
	HostName: root@127.0.0.1中的127.0.0.1
	User: root@127.0.0.1中的root
	identitiesOnly: 固有配置
	
退出后，配置即生效，这时候，你输入ssh hero就能访问远程服务器了。