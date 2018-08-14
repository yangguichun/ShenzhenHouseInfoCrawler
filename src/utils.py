import requests
import re
import datetime

class utils:
    @classmethod
    def add(cls, a, b):
        return a + b

    @classmethod
    def remove_blank_char(cls, str):
        return str.replace('\t','').replace('\n','').replace('\r','').replace(' ','').replace('\xa0','')

    @classmethod
    def get_num(self, text):
        nums = re.findall(r'\d+\.?\d+', text)
        if len(nums) > 0:
            return nums[0]
        else:
            return 0

    @classmethod
    def request_with_retry(cls, url, formdata=None, trycount=3):
        '''使用request请求数据，带重试功能'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}  # 请求头，模拟浏览器登陆
        for i in range(trycount):
            try:
                r = None
                if formdata is None:
                    r = requests.get(url, 'lxml', headers=headers)
                else:
                    r = requests.post(url, headers=headers, data=formdata)
                if r.status_code != requests.codes.ok:
                    cls.print('request_with_retry failed, url: {},  code: {}'.format(url, r.status_code))
                    return None
                return r
            except ConnectionError as err:
                cls.print('request_with_retry failed, url: {},  error: {}, retrycount: {}'.format(url, str(err), i))
            except:
                cls.print('request_with_retry failed, url: {}, retrycount: {}'.format(url, i))

        return None

    @classmethod
    def print(cls, str):
        print('{}, {}'.format(datetime.datetime.now(), str))
