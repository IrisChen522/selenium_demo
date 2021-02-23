# coding:utf-8
import requests

# # get
# kw = {'wd': 'pytest'}
# headers ={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36"}
# reponse = requests.get("http://www.baidu.com/s?", params = kw, headers = headers)
# print('text %s' %reponse.text)
# print('content %s' %reponse.content)
# print('url %s' %reponse.url)
# print('encoding %s' %reponse.encoding)
# print('status %s' %reponse.status_code)
#
#
# formdata = {
#     "type":"AUTO",
#     "i":"i love python",
#     "doctype":"json",
#     "xmlVersion":"1.8",
#     "keyfrom":"fanyi.web",
#     "ue":"UTF-8",
#     "action":"FY_BY_ENTER",
#     "typoResult":"true"
# }
#
# url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
# headers ={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36"}
# reponse = requests.post(url, data= formdata, headers = headers)
# print(reponse.text)
# print(reponse.json)

html = requests.get("http://www.baidu.com")
with open('test.txt','w',encoding='utf-8') as f:
    f.write(html.text)

ff=open('testt.txt','w',encoding='utf-8')
with open('test.txt', encoding='utf-8') as f:
    for line in f:
        ff.write(line)
        ff.close()