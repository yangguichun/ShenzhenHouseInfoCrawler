import requests
import re

class utils:
    @classmethod
    def remove_blank_char(cls, str):
        return str.replace('\t','').replace('\n','').replace('\r','')

    @classmethod
    def get_num(self, text):
        nums = re.findall(r'\d+\.?\d+', text)
        if len(nums) > 0:
            return nums[0]
        else:
            return 0

    @classmethod
    def request_with_retry(self, url, formdata=None, trycount=1):
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
                return r
            except ConnectionError as err:
                print('get {} location timeout, error: {}, retrycount: {}'.format(url, err, i))
            except:
                print('get {} location timeout, retrycount: {}'.format(url, i))

        return ''
