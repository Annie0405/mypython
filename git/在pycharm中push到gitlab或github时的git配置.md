# 在pycharm中push到gitlab或github时的git配置

## push到github

```shell
# 启用本地代理
git config --global http.proxy http://your_proxy:port
git config --global https.proxy http://your_proxy:port
# 将 your_proxy 和 port 替换为你的代理服务器地址和端口
# 在 设置 -> 网络和Internet -> 代理 中查询
```

## push到gitlab

```shell
# 查看代理配置
git config --global --get http.proxy
git config --global --get https.proxy
# 禁用本地代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```


