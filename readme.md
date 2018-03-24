练手小程序,从一个资源网站上搜索资源名称获取到百度云链接,然后分析百度云页面拿到相关参数请求真实下载地址将文件下载到本地
当前只下载pdf文件,遍历尝试下载搜索结果中的每一个百度云链接直到下载成功
## environment
python2/3

## 依赖
>tqdm(下载进度条),
>requests,
>BeautifulSoup

## run
```python 
python down.py bookName
```

## todo
- [ ] 验证码
- [ ] 百度云链接失效


