import json
import logging
import re
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main_handler(event, context):
    logger.info('got event{}'.format(event))
    sender = ""  # 修改1：填写发件人的邮件
    pass_ = ""  # 修改2：发件人邮箱授权码
    user = ""  # 修改3：收件人的邮件
    username = ""  # 修改4：手机号
    password = ""  # 修改5：密码

# 获取jwsession
    header = {
    "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us,en",
            "Connection": "keep-alive",
            "User-Agent": "",  # 修改6：User-Agent
            "Referer": "",  # 修改7：Referer
            "Content-Length": "360",
}
    loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    data = "{}"
    session = requests.session()
    url = loginUrl + "?username=" + username + "&password=" + password
    respt = session.post(url, data=data, headers=header)
    res = json.loads(respt.text)
    if res["code"] == 0:
        print("Login success.")
        jwsession = respt.headers['JWSESSION']
    else:
        print(res)
        print('Login failed.')

# 第一部分，获取定位打卡的ID和signID
# 获取ID和signID
    getheaders = {
        "Host": "student.wozaixiaoyuan.com",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": "",  # 修改6：User-Agent
        "Referer": "",  # 修改7：Referer
        "Content-Length": "500",
        "JWSESSION": str(jwsession),
}
    first = 'page=1&size=5'  # 获取id和signid所需要post的内容
    getapi = "http://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    getdata = requests.post(getapi, headers=getheaders,
                        data=first, ).json()  # 获取id和signid
    time.sleep(1)
    getdata = getdata['data']  # 获取返回值中的data数据
    a = str(getdata).replace("[", "")  # 去除中括号
    b = str(a).replace("]", "")
    c = b  # 交换变量
    d = re.findall(r"{(.+?)}", c)  # 利用正则去除大括号
    e = "{" + d[0] + "}"  # 获取第一项，并加上大括号
    e = eval(e)
    Fid = e['id']  # 提取id
    Lid = e['logId']  # 提取logid
    realdata = '{"id":' + Lid + "," + '"signId":' + Fid + "," + '''
    "latitude": "",
    "longitude": "",
    "country":"",
    "province":"",
    "city":"",
    "district":"",
     + "}"
    '''  # 修改7：打卡位置


# 第二部分，提交打卡
    api = "http://student.wozaixiaoyuan.com/sign/doSign.json/"
    signheaders = {
     "Host": "student.wozaixiaoyuan.com",
     "Content-Type": "application/json",
     "Accept-Encoding": "gzip, deflate, br",
     "Connection": "keep-alive",
     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",  # 修改5：User-Agent
     "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",  # 修改:7：Referer（相同）
     "Content-Length": "500",
     "Cookie": "",
     "JWSESSION": str(jwsession),  # 修改8：JWSESSION（相同）
 }
    res = requests.post(api, headers=signheaders,data=realdata.encode(), ).json()  # 打卡提交
    time.sleep(1)
    # 若打卡失败则发送邮件，成功不发
    if res['code'] == 0:
        print('success')
    else:
        print('faild')
        msg = MIMEText("打卡失败", 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["我在校园", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Me", user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡失败"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接

if __name__ == "__main__":
    main_handler()