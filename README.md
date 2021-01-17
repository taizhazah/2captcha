# 2captcha
Google  Verification code captcha
拿google的captcha来做测试：https://www.google.com/recaptcha/api2/demo
我们可以越过单独的captcha v2的格式，但是越不过steam的谷歌验证码，因为steam的谷歌验证码是企业版，但现在还是一个世界之谜，我训练了好几天，仅仅只是越过了captcha v2形式的验证。
切记切记切记：steam的话没有强大的机器学习，和反复机器学习的验证其他途径是越不过去的。


验证步骤：
1.准备chromedriver、selenium，或者requests。
在准备登陆目标网站之前发现有这个东西阻拦着我们。


2.当打开目标网页的时候，发现有滑块类|谷歌类验证码。
• 让我们打开网页调试查看源代码，查看此验证的元素查找以https://www.google.com/recaptcha/api2/demo开头的链接，或查找 data-sitekey参数。
• 让我们复制这个属性的值
我们使用了selenium中xpath自动提取，赋给 data-sitekey
• 让我们把这个属性的值发送至服务端，相当于告诉服务器我们遇到的哪一个验证。
3.让我们试下将验证发给服务器
请求接口:https://2captcha.com/in.php 让我们看看服务端需要我们发什么参数过去

按照我的操作
url = "http://2captcha.com/in.php?"
params = {
    'key': 'c************************a48',  # 服务的密钥
    'method': 'userrecaptcha',  # 直接赋值
    'googlekey': '6LfxxxxxxxxxxxxxxxxxxxxxRMFJYMz8',    # 从元素里复制下来的sitekey
    'pageurl': 'http://google.com/recaptcha/api2/demo', # 当前的url
    'json': 1# 拿到json形式的数据
}
>>{“status”：1，“request”：2123279149} # 证明成功了，我门只需要拿到request的值就能拿到返回
结果接口:https://2captcha.com/res.php
我们再看一下这个接口要求的参数是什么：

我们再来照猫画虎，构造url
url = "http://2captcha.com/res.php?"
params = {
    'key': 'c************************a48',  # 服务的密钥
    'action': 'get',  # 直接赋值
    'id': 2123279149,    # request值
    'json': 1
}
response = request(method='get', url=url+urlencode(params)).text
print(response)
我们就拿到了类似这么长的一个东西。

03AHJ_Vuve5Asa4koK3KSMyUkCq0vUFCR5Im4CwB7PzO3dCxIo11i53epEraq-uBO5mVm2XRikL8iKOWr0aG50sCuej9bXx5qcviUGSm4iK4NC_Q88flavWhaTXSh0VxoihBwBjXxwXuJZ-WGN5Sy4dtUl2wbpMqAj8Zwup1vyCaQJWFvRjYGWJ_TQBKTXNB5CCOgncqLetmJ6B6Cos7qoQyaB8ZzBOTGf5KSP6e-K9niYs772f53Oof6aJeSUDNjiKG9gN3FTrdwKwdnAwEYX-F37sI_vLB1Zs8NQo0PObHYy0b0sf7WSLkzzcIgW9GR0FwcCCm1P8lB-50GQHPEBJUHNnhJyDzwRoRAkVzrf7UkV8wKCdTwrrWqiYDgbrzURfHc2ESsp020MicJTasSiXmNRgryt-gf50q5BMkiRH7osm4DoUgsjc_XyQiEmQmxl5sqZP7aKsaE-EM00x59XsPzD3m3YI6SRCFRUevSyumBd7KmXE8VuzIO9lgnnbka4-eZynZa6vbB9cO3QjLH0xSG3-egcplD1uLGh79wC34RF49Ui3eHwua4S9XHpH6YBe7gXzz6_mv-o-fxrOuphwfrtwvvi2FGfpTexWvxhqWICMFTTjFBCEGEgj7_IFWEKirXW2RTZCVF0Gid7EtIsoEeZkPbrcUISGmgtiJkJ_KojuKwImF0G0CsTlxYTOU2sPsd5o1JDt65wGniQR2IZufnPbbK76Yh_KI2DY4cUxMfcb2fAXcFMc9dcpHg6f9wBXhUtFYTu6pi5LhhGuhpkiGcv6vWYNxMrpWJW_pV7q8mPilwkAP-zw5MJxkgijl2wDMpM-UUQ_k37FVtf-ndbQAIPG7S469doZMmb5IZYgvcB4ojqCW3Vz6Q

拿到这个怎么用呢？？

需要把我们拿到的token传给前端验证，并验证 。
wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
submit_js = 'document.getElementById("recaptcha-demo-form").submit();'
driver.execute_script(wirte_tokon_js)
time.sleep(1)
driver.execute_script(submit_js)

跳转成功页面，就恭喜你成功越过了。
以上操作都可通过selenium自动化完成，且若不能成功返回数据的，请看官方文档，里面详细的介绍的出现错误的类型及其解决方式。
源码已经附上，需要的可直接下载。
官方文档：www.sunxiaodou.icu
https://2captcha.com/2captcha-api#solving_recaptchav2_new
