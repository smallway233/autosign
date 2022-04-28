# 2022年4月23日23:41:27
# @author:Smallway
# name:定位打卡V3.0
import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
#注意，本代码仅供学习使用，请勿用于盈利等等，作者QQ1097123142，欢迎交流学习
#定位打卡V3.0版本（没有什么改进，就是从底层优化了代码，看起来更有逼格了而已（单纯的学会了怎么用字典......））
#此外，特别鸣谢@DominicKK在我学习的路上的帮助（即使我给他发消息他不理我（写到这时我看了一眼微信23:47，他回我了，时隔半小时（呵，懂了，还是不爱我）））
def main_handler(event, context):
    sender = "xxxx"  # 修改1：填写发件人的邮件
    pass_ = "xxxx"  # 修改2：发件人邮箱授权码
    user = "xxxx"  # 修改3：收件人的邮件
    username = "xxxx"  # 修改4：手机号
    password = "xxxx"  # 修改5：密码
    Referer="xxxx"#修改6：抓包获取
    User_Agent="xxxx"#修改7：抓包获取
    latitude=xxxx#修改8：纬度
    longitude=xxxx#修改9：经度
    country="中国"#修改10：一般不用改，我不信还有国外的要用，有的话我把我电脑屏幕吃了
    province="xxx省"#修改11：省份
    city="xx市"#修改12：城市
    district="xx区"#修改13：区县
    township="xx道"#修改14：街道
# 获取jwsession
    header = {
    "Host": "student.wozaixiaoyuan.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-us,en",
    "Connection": "keep-alive",
    "User-Agent": str(User_Agent),  
    "Referer": str(Referer),  
    "Content-Length": "360",
}
    loginUrl = "http://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    data = "{}"
    session = requests.session()
    url = loginUrl + "?username=" + username + "&password=" + password
    respt = session.post(url, data=data, headers=header)
    # @author:Smallway
    res = json.loads(respt.text)
    if res["code"] == 0:
        print("登录成功.")
        jwsession = respt.headers['JWSESSION']
    
    else:
        print(res['message'])

    getheaders = {
        "Host": "student.wozaixiaoyuan.com",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": str(User_Agent),
        "Referer": str(Referer),
        "Content-Length": "500",
        "JWSESSION": str(jwsession),
}
    first = 'page=1&size=5'  # 获取id和signid所需要post的内容
    getapi = "http://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    getdata = requests.post(getapi, headers=getheaders,
                        data=first, ).json()  # 获取id和signid
    time.sleep(1)
    getdata = getdata['data']  # 获取返回值中的data数据
    getdata=getdata[0]
    print(getdata)
    # @author:Smallway
    realdata = {
    "id":str(getdata['logId']),
    "signId":str(getdata['id']),
    "latitude":latitude,
    "longitude":longitude,
    "country":country,
    "province":province,
    "city":city,
    "district":district,
    "township":township,
    }
    print(realdata)
    api = "http://student.wozaixiaoyuan.com/sign/doSign.json/"
    signheaders = {
     "Host": "student.wozaixiaoyuan.com",
     "Content-Type": "application/json",
     "Accept-Encoding": "gzip, deflate, br",
     "Connection": "keep-alive",
     "User-Agent":str(User_Agent) ,
     "Referer": str(Referer),
     "Content-Length": "500",
     "Cookie": "",
     "JWSESSION": str(jwsession),
     "charset":"utf-8",
}
    res = requests.post(api, headers=signheaders,json=realdata)  # 打卡提交@author:Smallway
    time.sleep(1)
    res=eval(res.text)
    if res['code']==0:
        return "打卡成功"+str(res)
    else:
        msg = MIMEText("打卡失败原因为："+str(res.text), 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["我在校园", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Me", user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡失败"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
#此处请注意，本人写的是当打卡失败时发送邮件提醒，若想改成打卡成功也发送邮件，请将以下内容覆盖至101至111行（没有三引号奥）
"""
        msg = MIMEText("打卡情况："+str(res.text), 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["我在校园", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Me", user])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡失败"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, pass_)  # 发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
"""
if __name__ == "__main__":
    main_handler()
