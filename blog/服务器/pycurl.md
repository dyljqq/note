# pycurl在新版本mac中的安装

[原文](https://cscheng.info/2018/01/26/installing-pycurl-on-macos-high-sierra.html)

在新版本的mac中，安装pycurl会出现:

	__main__.ConfigurationError: Curl is configured to use SSL, but we have not been able to determine which SSL backend it is using. Please see PycURL documentation for how to specify the SSL backend manually.

解决办法:

	$ PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip install --no-cache-dir pycurl