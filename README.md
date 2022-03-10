# 我在校园定位签到
**友情提示：** 本文章及相关代码仅作为学习使用，使用者若以此进行盈利等，造成后果由使用者自负，均与作者无关。健康生活，认真打卡。作者[QQ 1097123142](tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=1097123142&website=www.oicqzone.com)，若学习过程中有相关疑问，欢迎交流。感谢[@dominic548](https://gitee.com/dominic548/autocheck)的帮助，特别鸣谢。

本教程灵感来源于生活。

​	此版本为2.0。版本1.0使用抓包获取到的 jwsession 进行登录，而此版本使用账号密码登录，以解决部分用户出现 jwsession 更新频率快的问题。版本1.0的弊端：每次 jwsession 后都需要重新抓取，再写入代码；版本2.0的弊端：代码时而会出现“账号密码错误”的报错，具体情况已在**《新版必读.txt》**中列出，**建议阅读**。两个版本各有利弊，均可正常使用，根据自己的实际情况使用即可。

​	**所有文件以及相关代码已在文件列表上传，下载即可使用**

<img src="https://gitee.com/dominic548/picgo/raw/master/uTools/2022213-130940-1644728979852.png" alt="image-20220213130917422" style="zoom:67%;" />

### 一、Fiddler 抓包工具

#### 1.安装和配置

安装包下载：Fiddler 安装包和 Fiddler 证书生成器

蓝奏云链接：https://dominic.lanzouq.com/iKszLzyh5gh

下载后解压，先双击 `FiddlerSetup.exe` 进行安装，另一个是证书生成器，暂时不用。

打开 Fiddler ，点击工具栏中的 `Tools` → `Options`

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802134532161-1627956867319.png" alt="1.1.1"  />

点击 `HTTPS` 标签，勾选框住的三项，然后点击右边的 `Actions`，选择第二项，会弹出一个弹窗，点击确定，之后点击 `OK` 完成设置

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802140021903.png" alt="1.1.2"  />

这时会发现桌面上多了一个证书文件（如下图），接下来马上会用到

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802140437482.png" alt="1.1.3"  />

打开电脑上任何一个浏览器，在这里我用的是 win10 自带的 Edge，打开设置，找到`证书管理`，实在找不到也可以直接搜索

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802140839373.png" alt="1.1.4"  />

点击`管理证书`，点击`导入`进入证书导入向导

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802141018230.png" alt="1.1.5" style="zoom:67%;" />

点击`下一页`继续

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802141144696.png" alt="1.1.6" style="zoom:67%;" />

点击`浏览`，选择要导入的文件

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802141332680.png" alt="1.1.7" style="zoom:67%;" />

在桌面找到刚刚导出的证书文件，点一下证书文件，选择`打开`

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802141716446.png" alt="1.1.8" style="zoom:67%;" />

之后一直点击`下一步`，直到完成证书导入。到这里配置工作基本完成，可以进行抓包了，刚刚导出在桌面的证书文件也可以删除

#### 2.抓包

接下来从微信电脑端打开我在校园小程序，然后打开日检日报或者健康打卡，会发现 Fiddler 中显示了很多内容，我们找到`student.wozaixiaoyuan.com`这一行，双击打开，在右边选择`Headers`标签，复制 `User-Agent（设备信息）`、`Referer（学校信息）`。

![1.2.1](https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802145622192.png)

复制的内容可以发给你的工具人小伙伴，或者你的小号，总之先保留下来备用。

### 二、QQ邮箱

#### 获取授权码

用QQ邮箱发件也需要登录，不是用账号密码，而是授权码（更安全），接下来获取授权码

进入QQ邮箱网页版，进入`设置`，选择`账户`

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802152812320.png" alt="2.1.1" style="zoom:67%;" />

往下翻找到 `POP3/SMTP服务`，确保第一项是`已开启`状态，如果不是，点击后面的开启，然后选择下面的`生成授权码`

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802152944128.png" alt="2.1.2" style="zoom:67%;" />

根据提示验证后，得到授权码，和抓包步骤一样，把授权码复制保存下来备用。

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802153128652.png" alt="2.1.3" style="zoom:67%;" />

### 三、Python 代码

#### 1.获取位置信息

代码中直接会填入打卡的地址，所以代码正常运行后，即使人不在学校，打卡也会在学校，这时候就要留意会不会穿帮了。

需要填写经纬度，可以通过百度的拾取坐标系统获取：[拾取坐标系统 (baidu.com)](https://api.map.baidu.com/lbsapi/getpoint/index.html)

<img src="https://gitee.com/dominic548/picgo/raw/master/uTools/2022213-132154-1644729713565.png" alt="3.1.1" style="zoom:67%;" />


#### 5.定位签到

#### 1.定位签到1.0版本（需要抓包）
```python
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

#### 2.定位签到2.0版本（打开公众号需要重新登陆）

```Python
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

### 四、腾讯云函数

注册过程就不再赘述，注册完记得完成实名认证，这里给出腾讯云官网链接：[腾讯云(tencent.com)](https://cloud.tencent.com/)

#### 1.使用云函数

进入腾讯云先登录，搜索云函数

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802160948779.png" alt="4.1.1" style="zoom:67%;" />

管理控制台

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802161241550.png" alt="4.1.2" style="zoom:67%;" />

函数服务 → 新建

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210802161459839.png" alt="4.1.3" style="zoom:67%;" />

选择自定义创建，函数名称可以改一下，方便区分，这里用健康打卡做例子，由于名称不能写中文，所以就写了健康打卡的拼音缩写

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803080018644.png" alt="4.1.4" style="zoom:67%;" />

往下翻，函数代码选择在线编辑，把刚刚编辑好的代码粘贴在这里

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803080356200.png" alt="4.1.5" style="zoom:67%;" />

其他设置保持默认即可，然后点击完成。这样就把代码部署在腾讯云上了，可以尝试运行一下，直接点击测试按钮，立马就能收到一封邮件，提示打卡状态

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803081027997.png" alt="4.1.6" style="zoom:67%;" />

![image-20210803081034094](https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803081034094.png)

#### 2.定时触发

设置定时触发之后，就可以按照自己的时间定时运行一次代码，这样就解放了双手

触发管理 → 创建触发器

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803083310441.png" alt="4.1.7" style="zoom:67%;" />

触发周期选择自定义，这里要输入 Cron 表达式，健康打卡是每天一次，只要过了零点就可以打卡，所以 Cron 表达式是 `0 01 00 * * * *`，表示每天00:01运行一次代码；日检日报是每天三次，这里根据我们学校的时间，我写的是 `0 35 6,12,19 * * * *`，表示每天6:35、12:35、19:35各运行一次；其他设置保持默认即可，点击提交。

教程到这里就结束了，如果需要其他时间打卡，可以直接更改 Cron表达式，为了方便大家更改，关于 Cron 表达式的语法在下面也讲解一下

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803083504283.png" alt="4.1.8" style="zoom:67%;" />

### 五、Q&A

最后在这里放一个问答板块，如果大家有什么问题可以在评论区提问（评论区可能回复不及时，推荐使用qq联系），我会定期更新在这里

#### 1.Cron表达式

Cron表达式有7个字段，以空格分割

| 第一位 | 第二位 | 第三位 | 第四位 | 第五位 | 第六位 | 第七位 |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- |
| 秒     | 分钟   | 小时   | 日     | 月     | 星期   | 年     |

每一位都有一定的取值范围

| 字段 | 值                                                           | 通配符  |
| :--- | :----------------------------------------------------------- | :------ |
| 秒   | 0 - 59的整数                                                 | , - * / |
| 分钟 | 0 - 59的整数                                                 | , - * / |
| 小时 | 0 - 23的整数                                                 | , - * / |
| 日   | 1 - 31的整数（需要考虑月的天数）                             | , - * / |
| 月   | 1 - 12的整数或 JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC | , - * / |
| 星期 | 0 - 6的整数或 SUN,MON,TUE,WED,THU,FRI,SAT。其中0指星期日，1指星期一，以此类推 | , - * / |
| 年   | 1970 - 2099的整数                                            | , - * / |

举例说明：

| 日检日报 |  0   |  35  |    6，12，19    |  *   |  *   |     *      |  *   |
| :------: | :--: | :--: | :-------------: | :--: | :--: | :--------: | :--: |
|   含义   | 0秒  | 35分 | 6时，12时，19时 | 每日 | 每月 | 每星期每天 | 每年 |

| 健康打卡 |  0   |  01  |  00  |  *   |  *   |     *      |  *   |
| :------: | :--: | :--: | :--: | :--: | :--: | :--------: | :--: |
|   含义   | 0秒  | 01分 | 0时  | 每日 | 每月 | 每星期每天 | 每年 |



#### 2.如何第一时间收到QQ邮件

如果每次都打开邮箱网页查看打卡状态，那自然很麻烦，最简单的方法就是手机下载QQ邮箱客户端，并打开消息提醒，这样每次代码运行结束都能及时收到打卡状态。如果不想下载软件，也可以用微信的QQ邮件提醒，不过这需要一些设置：

首先确保微信和QQ号已经绑定，找到【设置】-【账号与安全】-【更多安全设置】来绑定QQ号

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803090822826.png" alt="5.1.1" style="zoom:67%;" />

绑定好之后，点击微信上方的搜索，搜“QQ邮箱提醒”功能并启用，这样就可以在微信收到邮件了

<img src="https://gitee.com/dominic548/picgo/raw/master/Typora/image-20210803091352067.png" alt="5.1.2" style="zoom:67%;" />

#### 3.下载了QQ邮箱APP后，邮箱公众号收不到邮箱消息了

进入qq邮箱app，点开头像，选择新邮件提醒，拉到下面选择你的qq邮箱账号，然后关闭下面的仅在qq邮箱客户端提醒，然后公众号就可以正常接收信息了。

#### 4.errorcode

若出现类似于`{"errorCode":1,"errorMessage":"Traceback (most recent call last):\n ......,"statusCode":443} `的错误，可尝试重新建一个云函数，即重复`步骤四`





