import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import requests

# 常量
USER = {}
API_KEY = "账号的key值"


def open_google():
    from selenium.webdriver.chrome.options import Options
    chrome_option = Options()
    chrome_option.add_argument('--proxy-server=http://36.72.5.114:80')
    driver = webdriver.Chrome(executable_path=r'D:/chromedriver.exe', chrome_options=chrome_option)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    data_sitekey = driver.find_element_by_xpath('//*[@id="recaptcha-demo"]').get_attribute("data-sitekey")
    print(data_sitekey)
    page_url = "https://www.google.com/recaptcha/api2/demo"
    u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
    r1 = requests.get(u1)
    print(r1.json())
    rid = r1.json().get("request")
    u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
    time.sleep(25)
    while True:
        print(u2)
        r2 = requests.get(u2)
        print(r2.json())
        if r2.json().get("status") == 1:
            form_tokon = r2.json().get("request")
            break
        time.sleep(5)
    wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
    submit_js = 'document.getElementById("recaptcha-demo-form").submit();'
    driver.execute_script(wirte_tokon_js)
    time.sleep(1)
    driver.execute_script(submit_js)


if __name__ == '__main__':
    open_google()