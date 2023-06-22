import random
import http.client
import hashlib
import urllib.parse
import json

class Translation:
    def __init__(self):
        pass

    def baiduTranslate(self, translate_text, flag):
        """
        :param translate_text: Scentence need to be translated，len(q)<2000
        :param flag: 1:translate to English；0:translate to Chinese
        :return: Return the result
        For example:
        q=我今天好开心啊！
        result = {'from': 'zh', 'to': 'en', 'trans_result': [{'src': '我今天好开心啊！', 'dst': "I'm so happy today!"}]}
        """

        appid = '20230521001684441'
        secretKey = 'cGH2DJmmCQXILcT4pvOz'
        httpClient = None
        myurl = '/api/trans/vip/translate'
        fromLang = 'auto'  # original language

        if flag:
            toLang = 'en'  # Translate language
        else:
            toLang = 'zh'  # Translate language

        salt = random.randint(32768, 65536)

        sign = appid + translate_text + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
                '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

        # Create the connection and return the result
        try:
            httpClient = http.client.HTTPConnection('fanyi-api.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            # return result
            return result['trans_result'][0]['dst']

        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()

