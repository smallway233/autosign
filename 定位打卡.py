from email import message
import json
import logging
import requests, time
import smtplib
import re
from email.mime.text import MIMEText
from email.utils import formataddr
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main_handler(event, context):
    logger.info('got event{}'.format(event))
    sender="xxx"#修改1：填写发件人的邮件
    pass_="xxx"#修改2：发件人邮箱授权码
    user="xxx"#修改3：收件人的邮件

    getheaders = {
                "Host": "student.wozaixiaoyuan.com",
                "content-type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "User-Agent": "xxx",  # 修改4：User-Agent
                "Referer": "xxx",  # 修改5：Referer
                "Content-Length": "500",
                "JWSESSION": "xxx", #修改6：JWSESSION
            }
    first = 'page=1&size=5'
    getapi="http://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    getdata=requests.post(getapi,headers=getheaders,data=first,).json()
    time.sleep(1)
    getdata=getdata['data']
    a=str(getdata).replace("[", "");
    b=str(a).replace("]", "");
    c=b
    d=re.findall(r"{(.+?)}",c)
    e="{"+d[0]+"}"
    e=eval(e)
    Fid=e['id']
    Lid=e['logId']
    realdata='{"id":'+Lid+","+'"signId":'+Fid+","+'''
    "latitude":xxx,
    "longitude":xxx,
    "country":"xxx",
    "province":"xxx",
    "city":"xxx",
    "district":"xxx",
    "township":"xxx"'''+"}"#修改7：打卡位置

    api="http://student.wozaixiaoyuan.com/sign/doSign.json/"
    signheaders={
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "xxx",  # 修改8：User-Agent(相同)
            "Referer": "xxx",  # 修改:7：Referer（相同）
            "Content-Length": "500",
            "Cookie":"",
            "JWSESSION": "xxx",  # 修改8：JWSESSION（相同）
        }
    res = requests.post(api, headers=signheaders, data=realdata.encode(),).json()
    time.sleep(1)
    if res['code']==0:
        return '打卡成功'
    else:
        msg = MIMEText("打卡失败", 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["我在校园", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Me", user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡失败"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        return '打卡失败'


