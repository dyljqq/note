#安装pod

	 sudo gem install cocoapods
	 
会出现报错：

	Fetching: cocoapods-core-1.1.1.gem (100%)
	Successfully installed cocoapods-core-1.1.1
	Fetching: cocoapods-1.1.1.gem (100%)
	ERROR:  While executing gem ... (Errno::EPERM)
	    Operation not permitted - /usr/bin/pod
	    
解决办法:
	
	sudo gem install -n /usr/local/bin cocoapods

###安装库

	pod repo remove master
	pod setup
	pod install