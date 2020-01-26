'''
donke 2020/01/25 23:44
功能实现
'''
import json
import requests
from pypinyin import pinyin


# 拼音库用法
# https://www.cnblogs.com/felixwang2/p/9246281.html

# import BeautifulSoup


def up_int(n):
    '''
    整数化n
    :param n: 数字
    :return:None || int
    '''
    num = str(n)
    if num.isdigit():
        num = eval(num)
        if num == int(num):
            return num
        return num + 1
    return False


class GetChengYu:
    def __init__(self):
        self.api = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
        self.listNum = 43383
        self.rn = 30  # 每个页面的数量
        self.pn = 0  # 当前页面数量
        self.prams = {
            'pn': self.pn,  # 页面数
            'rn': self.rn,  # 单次个数
            'resource_id': 28204,
            'from_mid': 1,
            'format': 'json',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'query': '成语大全',
            'sort_key': '',
            'sort_type': 1,
            'stat0': '',
            'stat1': '',
            'stat2': '',
            'stat3': '',
            'cb': 'jQuery1102013400891090099654_1579965620395',
            '_': '1579965620416',
        }

    def get_data(self, cur_page_num=0):
        self.pn = cur_page_num
        self.prams['pn'] = cur_page_num*self.rn
        res = requests.get(self.api, params=self.prams).text
        res.encode('utf-8')
        try:
            data = json.loads(res.split('(')[1].split(')')[0])
            print(data)
            self.listNum = int(data['data'][0]['listNum'])
            return data
        except Exception as e:
            print('***************************error***************************')
            print(str(e))
            print('***************************error***************************')
            return None


temp = {'data': [
    {'display_title': '成语大全',
     'listNum': '43383',
     'result': [
         {'ename': '水深火热',
          'jumplink': 'https://hanyu.baidu.com/zici/s?wd=%E6%B0%B4%E6%B7%B1%E7%81%AB%E7%83%AD&query=%E6%88%90%E8%AF%AD%E5%A4%A7%E5%85%A8&srcid=28204&from=kg0'},
         {'ename': '鸟语花香',
          'jumplink': 'https://hanyu.baidu.com/zici/s?wd=%E9%B8%9F%E8%AF%AD%E8%8A%B1%E9%A6%99&query=%E6%88%90%E8%AF%AD%E5%A4%A7%E5%85%A8&srcid=28204&from=kg0'},
         {'ename': '自以为是',
          'jumplink': 'https://hanyu.baidu.com/zici/s?wd=%E8%87%AA%E4%BB%A5%E4%B8%BA%E6%98%AF&query=%E6%88%90%E8%AF%AD%E5%A4%A7%E5%85%A8&srcid=28204&from=kg0'}
     ]
     }
],
    'status': 0}

# session = requests.session()


