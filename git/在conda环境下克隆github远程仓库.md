# 在conda环境下克隆github远程仓库

## 克隆指令

```shell
git clone https://github.com/Annie0405/mypython.git
```

## 可能遇到的bug

```shell
fatal: unable to access 'https://github.com/Annie0405/mypython.git/': Failed to connect to github.com port 443 after 21088 ms: Couldn't connect to server
```

```shell
fatal: unable to access 'https://github.com/Annie0405/mypython.git/': schannel: CertGetCertificateChain trust error CERT_TRUST_IS_PARTIAL_CHAIN
```

解决方式（来源：https://www.cnblogs.com/chuanzhang053/p/17833661.html）：

```shell
# 跳过ssl的验证（有效）
git config --global http.sslVerify false
```

```shell
# 设置代理（不确定是否有效）
git config --global http.proxy http://your_proxy:port
git config --global https.proxy http://your_proxy:port
# 将 your_proxy 和 port 替换为你的代理服务器地址和端口
# 在 设置 -> 网络和Internet -> 代理 中查询
```

