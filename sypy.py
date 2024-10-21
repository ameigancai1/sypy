##.py 
import requests
import json
import re
import hashlib
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

paras = {
    "username": os.environ.get('USER'),
    "password": os.environ.get('PASSWORD'),
}

# https://ld246.com/login?goto=https://ld246.com/settings/point
headers = {
    'authority': 'ld246.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://ld246.com',
    'pragma': 'no-cache',
    'referer': 'https://ld246.com/login?goto=https://ld246.com/settings/point',
    'sec-ch-ua': '^\\^Not_A',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
    'x-requested-with': 'XMLHttpRequest',
}
headersCheckIn = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://ld246.com/settings/point',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
    'sec-ch-ua': '^\\^Not_A',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
}
headersDayliCheck = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://ld246.com/activity/checkin',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
    'sec-ch-ua': '^\\^Not_A',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
}

def getPara(name):
    return paras[name]


def setPara(name, value):

    paras[name] = value
    print(value)
    return value


log = ""


def appendLog(tempLog):
    global log
    log = log + "\n" + tempLog


def printLog():
    try:
        print("PUSHPLUS 服务启动")
        url = "http://www.pushplus.plus/send"
        data = {
            "token": os.environ.get('PUSHPLUS_TOKEN'),
            "title": "siyuan_Sign",
            "content": log
        }
        body = json.dumps(data).encode(encoding="utf-8")
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS 推送成功！")
        else:
            url_old = "http://pushplus.hxtrip.com/send"
            headers["Accept"] = "application/json"
            response = requests.post(url=url_old, data=body, headers=headers).json()
            if response["code"] == 200:
                print("PUSHPLUS(hxtrip) 推送成功！")
            else:
                print("PUSHPLUS 推送失败！")
    except:
        print(log)


def getMsg(htmltext):
    # print(htmltext)
    try:
        scoreGet = re.search("(今日签到获得.*积分)", htmltext).group(1)
        scoreGet = re.sub("<[^<]*>", "", scoreGet)

        scoreTotal = re.search("(积分余额[\s0-9]*)", htmltext).group(1)
        appendLog(scoreGet+"\n"+scoreTotal)
        getTopic()
    except:
        print("获取排行信息失败")


def getTopic():
    resp = session.get("https://ld246.com/top/checkin/today", data=data, headers=headersDayliCheck,
                       verify=False, proxies=proxy)
    # print(resp.text)
    index = re.search("([0-9]+)\.\s+<a[^<]+aria-name=\"" + getPara("username"), resp.text, re.S).group(1)
    #print(res)
    count = len(re.findall("([0-9]+)\.\s+<a[^<]+aria-name=\"", resp.text, re.S))
    #print(len(res))
    appendLog("今日奖励排行第"+index+",超过了"+str((1-int(index)/count)*100)+"%的人")
proxy = None
# proxy = {
#     "http": "127.0.0.1:9898",
#     "https": "127.0.0.1:9898"
# }

md5 = hashlib.md5(getPara("password").encode(encoding='utf-8')).hexdigest()
data = '{"nameOrEmail":' + getPara("username") + ',"userPassword":' + md5 + ',"captcha":""}'
session = requests.session()
response = session.post('https://ld246.com/login?goto=https://ld246.com/settings/point', data=data, headers=headers,
                        verify=False, proxies=proxy)
print("login msg:" + response.text)
tokenName = response.json()["tokenName"]
token = response.json()["token"]

cookie = {tokenName: token}

response = session.get("https://ld246.com/activity/checkin", cookies=cookie, proxies=proxy, headers=headersCheckIn,
                       verify=False)

if response.text.find("领取今日签到奖励") >= 0:
    res = re.findall(r"<a href=\"([^>^\"]*)\"[^>]*>领取今日签到奖励</a>", response.text, re.S)
    if len(res) > 0:
        print(res[0])
        appendLog("开始签到")

        response = session.get(res[0], proxies=proxy, headers=headersDayliCheck,
                               verify=False)
        if response.text.find("今日签到获得") >= 0:
            appendLog("签到成功")
            getMsg(response.text)

    else:
        appendLog("未找到签到链接")
elif response.text.find("今日签到获得") >= 0:
    appendLog("已经签到过了")
    getMsg(response.text)
else:
    print(response.text)
    appendLog("签到异常")
printLog()

# def pushplus_bot(title: str, content: str) -> None:
#     """
#     通过 push+ 推送消息。
#     """
#     if not push_config.get("PUSH_PLUS_TOKEN"):
#         print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
#         return
#     print("PUSHPLUS 服务启动")

#     url = "http://www.pushplus.plus/send"
#     data = {
#         "token": push_config.get("PUSH_PLUS_TOKEN"),
#         "title": title,
#         "content": content,
#         "topic": push_config.get("PUSH_PLUS_USER"),
#     }
#     body = json.dumps(data).encode(encoding="utf-8")
#     headers = {"Content-Type": "application/json"}
#     response = requests.post(url=url, data=body, headers=headers).json()

#     if response["code"] == 200:
#         print("PUSHPLUS 推送成功！")

#     else:

#         url_old = "http://pushplus.hxtrip.com/send"
#         headers["Accept"] = "application/json"
#         response = requests.post(url=url_old, data=body, headers=headers).json()

#         if response["code"] == 200:
#             print("PUSHPLUS(hxtrip) 推送成功！")

#         else:
#             print("PUSHPLUS 推送失败！")

