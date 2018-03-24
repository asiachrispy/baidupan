# coding:utf-8
import re

import requests
import sys
from bs4 import BeautifulSoup
from baidu import baidu


class walksmile():
    client = requests.session()
    version2 = sys.version_info < (3, 4)

    def search(self, keyword):
        url = r'http://walksmile.com/search?q={}&cat=2&size=30'
        result = self.client.get(url.format(keyword))
        bs = BeautifulSoup(result.text, "html.parser")
        list_ = bs.find_all(class_='media-body')
        array = []
        for item in list_:
            if self.version2:
                matching = re.search(keyword, item.h4.text.encode('utf-8'))
                num = item.span.text.encode('utf-8').replace('点击数：', '')
            else:
                matching = re.search(keyword, item.h4.text)
                num = item.span.text.replace('点击数：', '')
            if not matching:  # 垃圾网站按单个字符匹配的
                continue
            array.append({
                'times': int(num),
                'link': 'http://walksmile.com' + item.a.attrs['href']
            })
        if len(array) == 0:
            print('没有搜索到匹配的结果')
            exit(0)
        array.sort(key=lambda k: (k.get('times', 0)))  # 按照下载次数排序
        i = 1
        print('当前只搜索前30条结果,将按照点击数降序依次尝试下载,下载成功将退出本程序')
        while True:
            print("开始尝试下载第{}个搜索结果".format(i))
            url = array.pop()['link']
            result = self.client.get(url)
            bs = BeautifulSoup(result.text, "html.parser")
            list_ = bs.find_all(type='button', text='点我')
            bd = baidu()
            for (index, item) in enumerate(list_):
                print("     开始尝试第{}个百度云链接".format(index + 1))
                arr = item.attrs
                if arr['data-shorturl']:
                    res = bd.excute(arr['data-shorturl'])
                else:
                    res = bd.excute(
                        "https://pan.baidu.com/share/link?uk={}&shareid={}".format(arr['data-uk'], arr['data-fileid']))
                if res:
                    return True
            i += 1


if __name__ == '__main__':
    fileName = sys.argv[1]
    obj = walksmile()
    obj.search(fileName)
