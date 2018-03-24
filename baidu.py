# coding:utf-8
import requests
import re
import json
import sys
from tqdm import tqdm


class baidu():
    client = requests.session()
    version2 = sys.version_info < (3, 4)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }

    def getCookie(self):
        return self.client.get('http://www.baiud.com', headers=self.headers)

    def getParams(self, url):
        content = self.client.get(url, headers=self.headers, cookies=self.client.cookies)
        content.encoding = 'utf-8'
        pattern = r'(?<=sign":").*?(?=","public")|(?<=timestamp":).*?(?=,"timeline_status")|(?<="bdstoken":).*?(?=,"is_vip)|(?<="uk":).*?(?=,"task_key")|(?<="shareid":).*?(?=,"sign)|(?<="fs_id":).*?(?=,"app_id)'
        return re.findall(pattern, content.text)

    def getRealLink(self, params, url):
        _url = r'https://pan.baidu.com/api/sharedownload?sign={}&timestamp={}&bdstoken={}&channel=chunlei&clienttype=0&web=1&app_id=250528'
        data = {
            'encrypt': '0',
            'product': 'share',
            'uk': params[1],
            'primaryid': params[4],
            'fid_list': "[{}]".format(params[0])
        }
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Content-Length': '',
            'Origin': 'https://pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url,
        }
        content = self.client.post(_url.format(params[5], params[3], params[2]), headers=headers,
                                   cookies=self.client.cookies, data=data)
        return json.loads(content.text)

    def download(self, url, fileName):
        response = self.client.get(url, headers=self.headers, cookies=self.client.cookies, stream=True)
        size = int(response.headers.get('Content-Length')) / 1024
        with open('./files/' + fileName, 'wb')as f:
            print("开始下载 {}".format(fileName.encode('utf-8') if self.version2 else fileName))
            print("总大小：{}KB".format(size))
            for item in tqdm(iterable=response.iter_content(1024), total=size, unit='k'):
                f.write(item)
            print("{} has downloaded！".format(fileName.encode('utf-8') if self.version2 else fileName))
            return True

    def excute(self, url):
        self.getCookie()
        params = self.getParams(url)
        js = self.getRealLink(params, url)
        if (js['errno'] != 0):
            print('请求太频繁,请稍后再试')
            return False
        else:
            return self.download(js["list"][0]['dlink'], js['list'][0]['server_filename'])
